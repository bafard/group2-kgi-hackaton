"""
Ollama API Routes
Test and manage Ollama local LLM connection.
"""

from fastapi import APIRouter, HTTPException
import logging
from ..utils.ollama_service import ollama_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/test-connection")
async def test_ollama_connection():
    """Test connection to Ollama server."""
    try:
        result = await ollama_service.test_connection()
        logger.info(f"🦙 Ollama connection test: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ Ollama connection test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_ollama_models():
    """List available models in Ollama."""
    try:
        if not await ollama_service.is_available():
            raise HTTPException(status_code=503, detail="Ollama server not available")
        
        models = await ollama_service.list_models()
        return {
            "available_models": models,
            "default_model": ollama_service.model_name,
            "base_url": ollama_service.base_url
        }
    except Exception as e:
        logger.error(f"❌ Failed to list Ollama models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-chat")
async def test_ollama_chat(message: dict):
    """Test chat with Ollama."""
    try:
        if not await ollama_service.is_available():
            raise HTTPException(status_code=503, detail="Ollama server not available")
        
        test_messages = [
            {"role": "user", "content": message.get("content", "Hello, are you working?")}
        ]
        
        response = await ollama_service.generate_chat_completion(test_messages)
        return {
            "status": "success",
            "response": response["choices"][0]["message"]["content"],
            "model": response["model"],
            "usage": response["usage"]
        }
        
    except Exception as e:
        logger.error(f"❌ Ollama chat test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))