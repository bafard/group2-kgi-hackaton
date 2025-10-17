from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os
# Force using mock service for now due to dependency issues
from ..utils.mock_sql_rag_service import sql_rag_service
from ..utils.chat_service import chat_service
from ..utils.local_llm_service import local_llm_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models
class RAGQueryRequest(BaseModel):
    query: str
    include_context: bool = True
    max_context_items: int = 5

class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    context_used: Dict[str, Any]
    sources_count: Dict[str, int]
    processing_time_ms: int

class RAGRefreshResponse(BaseModel):
    success: bool
    message: str
    machine_records: int
    lifetime_records: int
    last_refresh: str

@router.post("/refresh-data", response_model=RAGRefreshResponse)
async def refresh_rag_data(background_tasks: BackgroundTasks):
    """
    Refresh RAG data from SQL Server and rebuild vector indexes
    """
    try:
        logger.info("🔄 Starting RAG data refresh...")
        
        # Run refresh in background for better performance
        result = sql_rag_service.refresh_data_and_vectors()
        
        return RAGRefreshResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ RAG refresh failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh RAG data: {str(e)}")

@router.post("/query", response_model=RAGQueryResponse)
async def query_rag_system(request: RAGQueryRequest):
    """
    Query the RAG system with machine tracking and UC lifetime data
    """
    try:
        import time
        start_time = time.time()
        
        logger.info(f"🔍 Processing RAG query: {request.query[:100]}...")
        
        # Search for relevant context
        context_results = sql_rag_service.search_relevant_context(
            request.query, 
            top_k=request.max_context_items
        )
        
        # Prepare context for LLM
        if request.include_context:
            system_prompt = """
You are an expert assistant for Komatsu undercarriage monitoring and machine diagnostics. 
You have access to real-time data from machine tracking systems and undercarriage component lifetime data.

Your role is to:
1. Analyze machine performance and maintenance data
2. Provide insights on undercarriage component wear and lifetime
3. Make recommendations for maintenance scheduling
4. Help with troubleshooting and predictive maintenance

When answering questions:
- Use the provided data context to give specific, accurate information
- Include relevant machine IDs, serial numbers, and component details when available
- Provide actionable recommendations when appropriate
- If data is insufficient, clearly state what additional information would be helpful
- Always be precise with numbers, dates, and technical specifications

Context Data Available:
{context}
"""
            
            formatted_context = context_results['combined_context']
            full_system_prompt = system_prompt.format(context=formatted_context)
            
            # Generate response using Azure OpenAI with context
            messages = [
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": request.query}
            ]
        else:
            # Generate response without specific context
            messages = [
                {"role": "system", "content": "You are an expert assistant for Komatsu undercarriage monitoring and machine diagnostics."},
                {"role": "user", "content": request.query}
            ]
        
        # Get AI response using chat service
        chat_response = await chat_service.chat_completion(messages)
        ai_response = chat_response['response']
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        # Prepare response
        response = RAGQueryResponse(
            query=request.query,
            answer=ai_response,
            context_used={
                'machine_results_count': len(context_results['machine_results']),
                'lifetime_results_count': len(context_results['lifetime_results']),
                'context_included': request.include_context,
                'total_context_length': len(context_results['combined_context'])
            },
            sources_count={
                'machine_tracking': len(context_results['machine_results']),
                'uc_lifetime': len(context_results['lifetime_results'])
            },
            processing_time_ms=processing_time
        )
        
        logger.info(f"✅ RAG query completed in {processing_time}ms")
        return response
        
    except Exception as e:
        logger.error(f"❌ RAG query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process RAG query: {str(e)}")

@router.get("/search-context/{query}")
async def search_context_only(query: str, max_items: int = 5):
    """
    Search for relevant context without generating an AI response
    """
    try:
        logger.info(f"🔍 Searching context for: {query[:100]}...")
        
        results = sql_rag_service.search_relevant_context(query, top_k=max_items)
        
        return {
            'query': query,
            'machine_results': results['machine_results'],
            'lifetime_results': results['lifetime_results'],
            'context_summary': results['combined_context'][:500] + '...' if len(results['combined_context']) > 500 else results['combined_context']
        }
        
    except Exception as e:
        logger.error(f"❌ Context search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search context: {str(e)}")

@router.get("/stats")
async def get_rag_stats():
    """
    Get current RAG system statistics including LLM providers
    """
    try:
        stats = sql_rag_service.get_system_stats()
        
        # Check local LLM availability
        local_llm_available = False
        local_llm_status = "disabled"
        
        if local_llm_service.enabled:
            try:
                local_llm_available = await local_llm_service.is_available()
                local_llm_status = "available" if local_llm_available else "unavailable"
            except Exception:
                local_llm_status = "error"
        
        return {
            'system_status': 'operational' if stats['has_machine_index'] or stats['has_lifetime_index'] else 'needs_refresh',
            'llm_providers': {
                'local_llm': {
                    'enabled': local_llm_service.enabled,
                    'available': local_llm_available,
                    'status': local_llm_status,
                    'model': local_llm_service.model,
                    'endpoint': local_llm_service.endpoint
                },
                'azure_openai': {
                    'configured': chat_service is not None,
                    'status': 'configured' if chat_service else 'not_configured'
                }
            },
            **stats
        }
    except Exception as e:
        logger.error(f"❌ Failed to get RAG stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get RAG stats: {str(e)}")

@router.get("/sample-queries")
async def get_sample_queries():
    """
    Get sample queries that work well with the RAG system
    """
    return {
        'machine_tracking_queries': [
            "What machines need maintenance soon?",
            "Show me the status of all excavators",
            "Which machines have the highest operating hours?",
            "What's the fuel consumption for machine XYZ?",
            "Which machines are currently at job site ABC?"
        ],
        'uc_lifetime_queries': [
            "Which undercarriage components need replacement?",
            "Show me components with less than 20% life remaining",
            "What's the wear rate for track chains?",
            "Which UC components are overdue for inspection?",
            "What are the replacement costs for worn components?"
        ],
        'combined_analysis_queries': [
            "Analyze the maintenance needs across all machines",
            "Which machines have both high hours and worn UC components?",
            "Create a maintenance priority report",
            "Show cost analysis for upcoming replacements",
            "Predict which machines will need attention next month"
        ]
    }

@router.get("/llm-status")
async def get_llm_status():
    """
    Get detailed status of all LLM providers
    """
    try:
        local_status = local_llm_service.get_status()
        local_available = False
        
        if local_status['enabled']:
            try:
                local_available = await local_llm_service.is_available()
            except Exception as e:
                local_status['error'] = str(e)
        
        return {
            'local_llm': {
                **local_status,
                'available': local_available,
                'priority': 'primary' if os.getenv("USE_LOCAL_LLM_FIRST", "true").lower() == "true" else 'secondary'
            },
            'azure_openai': {
                'configured': chat_service is not None,
                'priority': 'secondary' if os.getenv("USE_LOCAL_LLM_FIRST", "true").lower() == "true" else 'primary'
            },
            'fallback_mock': {
                'enabled': os.getenv("FALLBACK_TO_MOCK", "true").lower() == "true"
            }
        }
    except Exception as e:
        logger.error(f"❌ Failed to get LLM status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get LLM status: {str(e)}")

@router.post("/test-local-llm")
async def test_local_llm():
    """
    Test local LLM connectivity and response
    """
    if not local_llm_service.enabled:
        raise HTTPException(status_code=400, detail="Local LLM is not enabled")
    
    try:
        if not await local_llm_service.is_available():
            raise HTTPException(status_code=503, detail="Local LLM is not available")
        
        # Test simple generation
        test_response = await local_llm_service.chat_completion([
            {"role": "user", "content": "Hello! Please respond with 'Local LLM is working correctly.'"}
        ])
        
        return {
            'status': 'success',
            'model': local_llm_service.model,
            'endpoint': local_llm_service.endpoint,
            'test_response': test_response['response'],
            'usage': test_response['usage']
        }
        
    except Exception as e:
        logger.error(f"❌ Local LLM test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Local LLM test failed: {str(e)}")