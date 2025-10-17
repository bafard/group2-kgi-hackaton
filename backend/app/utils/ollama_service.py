"""
Ollama Local LLM Service
Handles communication with local Ollama server running Llama models.
"""

import logging
import httpx
import json
from typing import Dict, List, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, base_url: str = None):
        # Use host.docker.internal for Docker containers on Windows/Mac
        self.base_url = base_url or "http://host.docker.internal:11434"
        self.model_name = "llama3.2:3b"  # Default model
        self.timeout = 30.0
        self._available_models = []
        
    async def is_available(self) -> bool:
        """Check if Ollama server is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False
    
    async def list_models(self) -> List[str]:
        """Get list of available models."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
        return []
    
    async def get_available_model(self) -> str:
        """Get the first available model or default."""
        try:
            if not self._available_models:
                self._available_models = await self.list_models()
            
            if self._available_models:
                # Prefer llama models
                llama_models = [m for m in self._available_models if 'llama' in m.lower()]
                if llama_models:
                    return llama_models[0]
                return self._available_models[0]
            
            return self.model_name
        except:
            return self.model_name

    async def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate chat completion using Ollama."""
        
        model_to_use = model or await self.get_available_model()
        
        # Convert messages to Ollama format
        prompt = self._convert_messages_to_prompt(messages)
        
        payload = {
            "model": model_to_use,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Format response to match OpenAI-like structure
                    return {
                        "choices": [{
                            "message": {
                                "role": "assistant",
                                "content": result.get("response", "")
                            },
                            "finish_reason": "stop"
                        }],
                        "usage": {
                            "prompt_tokens": len(prompt.split()),
                            "completion_tokens": len(result.get("response", "").split()),
                            "total_tokens": len(prompt.split()) + len(result.get("response", "").split())
                        },
                        "model": model_to_use
                    }
                else:
                    logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                    raise Exception(f"Ollama API returned status {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            raise Exception(f"Failed to generate response from Ollama: {str(e)}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a single prompt for Ollama."""
        
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        # Add final assistant prompt
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to Ollama and return status info."""
        try:
            is_available = await self.is_available()
            
            if is_available:
                models = await self.list_models()
                return {
                    "status": "connected",
                    "base_url": self.base_url,
                    "available_models": models,
                    "default_model": self.model_name,
                    "model_exists": self.model_name in models
                }
            else:
                return {
                    "status": "disconnected",
                    "base_url": self.base_url,
                    "error": "Cannot connect to Ollama server"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "base_url": self.base_url,
                "error": str(e)
            }

# Global instance
ollama_service = OllamaService()