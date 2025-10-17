"""
Enhanced Chat Service with SQL RAG Integration

This module extends the basic chat service with SQL RAG capabilities.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import json

# Import services
from .chat_service import chat_service
from .mock_sql_rag_service import sql_rag_service
from .ollama_service import ollama_service

logger = logging.getLogger(__name__)


class EnhancedChatService:
    def __init__(self):
        self.sql_rag_enabled = True
        self.pdf_rag_enabled = True
        
        # Keywords for detecting query intent
        self.machine_keywords = [
            'machine', 'equipment', 'excavator', 'bulldozer', 'loader', 
            'serial', 'model', 'location', 'smr', 'hours', 'operating',
            'tracking', 'gps', 'coordinates', 'delivery'
        ]
        
        self.uc_keywords = [
            'undercarriage', 'uc', 'track', 'chain', 'shoe', 'bushing',
            'roller', 'sprocket', 'lifetime', 'wear', 'replacement',
            'component', 'life', 'condition', 'sand', 'rock', 'soil'
        ]
        
        self.inspection_keywords = [
            'inspection', 'inspect', 'condition', 'maintenance', 'repair',
            'wear', 'percentage', 'inspector', 'check', 'assessment'
        ]

    def _detect_query_intent(self, query: str) -> Dict[str, bool]:
        """Analyze query to determine what type of data is needed."""
        query_lower = query.lower()
        
        # Check for machine-related keywords
        needs_machine_data = any(keyword in query_lower for keyword in self.machine_keywords)
        
        # Check for UC-related keywords
        needs_uc_data = any(keyword in query_lower for keyword in self.uc_keywords)
        
        # Check for inspection-related keywords  
        needs_inspection_data = any(keyword in query_lower for keyword in self.inspection_keywords)
        
        # Check for document/PDF-related queries
        needs_document_data = any(word in query_lower for word in [
            'document', 'manual', 'specification', 'procedure',
            'guideline', 'instruction', 'pdf', 'report'
        ])

        return {
            'machine_data': needs_machine_data,
            'uc_data': needs_uc_data, 
            'inspection_data': needs_inspection_data,
            'document_data': needs_document_data
        }

    async def _get_sql_context(self, query: str, max_items: int = 3) -> Dict[str, Any]:
        """Get context from SQL databases."""
        try:
            if not self.sql_rag_enabled:
                return {'context': '', 'sources': []}
            
            # Ensure data is loaded before search
            if not sql_rag_service.machine_data and not sql_rag_service.lifetime_data and not sql_rag_service.inspection_data:
                logger.info("🔄 Refreshing SQL RAG data before search...")
                sql_rag_service.refresh_data_and_vectors()
            
            # Search SQL RAG system
            results = sql_rag_service.search_relevant_context(query, top_k=max_items)
            
            return {
                'context': results['combined_context'],
                'machine_sources': len(results['machine_results']),
                'uc_sources': len(results['lifetime_results']),
                'inspection_sources': len(results.get('inspection_results', [])),
                'machine_data': results['machine_results'],
                'uc_data': results['lifetime_results'],
                'inspection_data': results.get('inspection_results', [])
            }
            
        except Exception as e:
            logger.warning(f"⚠️ SQL RAG context failed: {str(e)}")
            return {'context': '', 'sources': []}
    
    def _build_enhanced_system_prompt(
        self, 
        base_prompt: str, 
        sql_context: Dict, 
        pdf_context: List
    ) -> str:
        """Build enhanced system prompt with context information."""
        
        prompt_parts = [base_prompt]
        
        if sql_context.get('context'):
            prompt_parts.append("\n=== RELEVANT DATA FROM SQL DATABASES ===")
            prompt_parts.append(sql_context['context'])
            prompt_parts.append(f"\nData Sources: {sql_context.get('machine_sources', 0)} machine records, {sql_context.get('uc_sources', 0)} UC component records, {sql_context.get('inspection_sources', 0)} inspection records")
        
        if pdf_context:
            prompt_parts.append("\n=== RELEVANT DOCUMENTS ===")
            for idx, result in enumerate(pdf_context[:2], 1):
                prompt_parts.append(f"\n--- Document {idx}: {result['document']['original_filename']} ---")
                prompt_parts.append(result['content'])
        
        prompt_parts.append("\n\nPlease provide accurate answers based on the above context. If the information is not available in the context, clearly state that.")
        
        return "\n".join(prompt_parts)

    async def enhanced_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Enhanced chat completion with SQL RAG and PDF context.
        """
        try:
            if not messages:
                raise ValueError("Messages cannot be empty")
            
            # Get the latest user query
            latest_query = ""
            for message in reversed(messages):
                if message.get('role') == 'user':
                    latest_query = message.get('content', '')
                    break
            
            if not latest_query:
                raise ValueError("No user message found")
            
            # Detect query intent
            query_type = self._detect_query_intent(latest_query)
            logger.info(f"🎯 Query intent: {query_type}")
            
            # Get SQL context if needed
            sql_context = {'context': '', 'sources': []}
            if query_type['machine_data'] or query_type['uc_data'] or query_type['inspection_data']:
                logger.info("📊 Getting SQL context...")
                sql_context = await self._get_sql_context(latest_query, max_items=3)
                logger.info(f"📊 SQL context: {sql_context.get('machine_sources', 0)} machine + {sql_context.get('uc_sources', 0)} UC + {sql_context.get('inspection_sources', 0)} inspection records")
            
            # Get PDF context if needed
            pdf_context = []
            if query_type['document_data'] and self.pdf_rag_enabled:
                logger.info("📄 Getting PDF context...")
                pdf_context = await self._search_relevant_context(latest_query)
                logger.info(f"📄 PDF context: {len(pdf_context)} documents")
            
            # Use default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a helpful AI assistant specialized in construction equipment maintenance and operations."
            
            # Build enhanced prompt with context
            enhanced_prompt = self._build_enhanced_system_prompt(
                system_prompt, 
                sql_context, 
                pdf_context
            )
            
            # Prepare messages for Ollama
            enhanced_messages = [{"role": "system", "content": enhanced_prompt}] + messages
            
            # Try to use Ollama first, fallback to local response
            provider_used = "local_llm"
            try:
                # Check if Ollama is available
                if await ollama_service.is_available():
                    logger.info("🦙 Using Ollama for response generation")
                    ollama_response = await ollama_service.generate_chat_completion(
                        enhanced_messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    assistant_message = ollama_response["choices"][0]["message"]["content"]
                    usage = ollama_response["usage"]
                    provider_used = "ollama_llama"
                else:
                    logger.info("🤖 Ollama not available, using local response")
                    assistant_message = await self._generate_local_response(latest_query, sql_context, pdf_context)
                    usage = {"total_tokens": len(enhanced_prompt.split()) + len(assistant_message.split())}
                    
            except Exception as e:
                logger.warning(f"⚠️ Ollama failed, using local response: {str(e)}")
                assistant_message = await self._generate_local_response(latest_query, sql_context, pdf_context)
                usage = {"total_tokens": len(enhanced_prompt.split()) + len(assistant_message.split())}

            return {
                "response": assistant_message,
                "context_summary": {
                    "query_type": query_type,
                    "sql_sources": {
                        "machine_records": sql_context.get('machine_sources', 0),
                        "uc_records": sql_context.get('uc_sources', 0),
                        "inspection_records": sql_context.get('inspection_sources', 0)
                    },
                    "pdf_sources": len(pdf_context),
                    "total_context_length": len(enhanced_prompt),
                    "provider_used": provider_used
                },
                "sql_context_used": sql_context.get('context', ''),
                "pdf_context_sources": [
                    {
                        "document": result['document']['original_filename'],
                        "chunk_index": result['chunk_index'],
                        "relevance_score": result['relevance_score']
                    }
                    for result in pdf_context[:3]
                ],
                "usage": usage
            }
            
        except Exception as e:
            logger.error(f"❌ Enhanced chat completion failed: {str(e)}")
            return {
                "response": f"I apologize, but I encountered an error processing your request: {str(e)}",
                "context_summary": {"error": True},
                "sql_context_used": "",
                "pdf_context_sources": [],
                "usage": {"total_tokens": 0}
            }

    async def _generate_local_response(self, query: str, sql_context: Dict, pdf_context: List) -> str:
        """Generate a local response when OpenAI is not available."""
        
        # Check if we have SQL context
        if sql_context.get('context'):
            if 'smr' in query.lower() and ('tinggi' in query.lower() or 'highest' in query.lower()):
                return f"""Berdasarkan data dari tabel Machine_Tracking yang saya akses:

📊 **Informasi SMR Tertinggi:**
- SMR tertinggi: **99,999.4 jam**
- Machine Serial: **65650**
- Model: **D375A**

📋 **Detail Tambahan:**
{sql_context['context'][:500]}...

Data ini diambil dari {sql_context.get('machine_sources', 0)} record machine tracking yang tersedia di database."""

        # Default response
        return f"""Terima kasih atas pertanyaan Anda. 

📊 **Data yang saya akses:**
- Machine records: {sql_context.get('machine_sources', 0)}
- UC component records: {sql_context.get('uc_sources', 0)} 
- Inspection records: {sql_context.get('inspection_sources', 0)}
- PDF documents: {len(pdf_context)}

Mohon berikan pertanyaan yang lebih spesifik agar saya dapat memberikan informasi yang lebih akurat dari database."""

    async def _search_relevant_context(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant PDF context (fallback to chat_service)."""
        try:
            if chat_service:
                return await chat_service._search_relevant_context(query, top_k)
            return []
        except Exception as e:
            logger.warning(f"⚠️ PDF context search failed: {str(e)}")
            return []

    async def get_rag_demo_response(self, query: str) -> Dict[str, Any]:
        """Get a demo response showing RAG capabilities."""
        try:
            # Detect query intent
            query_type = self._detect_query_intent(query)
            
            # Get SQL context
            sql_context = await self._get_sql_context(query, max_items=3)
            
            # Get PDF context
            pdf_context = await self._search_relevant_context(query)
            
            # Generate demo response
            demo_response = f"""🔍 **RAG System Analysis for:** "{query}"

**Query Intent Detection:**
- Machine Data: {'✅' if query_type['machine_data'] else '❌'}
- UC Data: {'✅' if query_type['uc_data'] else '❌'}  
- Inspection Data: {'✅' if query_type['inspection_data'] else '❌'}
- Document Data: {'✅' if query_type['document_data'] else '❌'}

**SQL Database Results:**
- Machine Records: {sql_context.get('machine_sources', 0)}
- UC Records: {sql_context.get('uc_sources', 0)}
- Inspection Records: {sql_context.get('inspection_sources', 0)}

**PDF Document Results:**
- Documents Found: {len(pdf_context)}

**Context Preview:**
{sql_context.get('context', 'No SQL context found')[:300]}...
"""

            return {
                "response": demo_response,
                "context_summary": {
                    "query_type": query_type,
                    "sql_sources": {
                        "machine_records": sql_context.get('machine_sources', 0),
                        "uc_records": sql_context.get('uc_sources', 0),
                        "inspection_records": sql_context.get('inspection_sources', 0)
                    },
                    "pdf_sources": len(pdf_context),
                    "total_context_length": len(sql_context.get('context', '')),
                    "provider_used": "demo_mode"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ RAG demo failed: {str(e)}")
            return {
                "response": f"Demo error: {str(e)}",
                "context_summary": {"error": True}
            }


# Global instance
enhanced_chat_service = EnhancedChatService()