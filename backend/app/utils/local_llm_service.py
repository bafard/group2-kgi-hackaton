"""
Local LLM Service untuk RAG system.
Support untuk Ollama dan local LLM lainnya sebagai alternatif Azure OpenAI.
"""

import os
import json
import asyncio
import aiohttp
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class LocalLLMService:
    """Service untuk berkomunikasi dengan Local LLM (Ollama, etc.)"""
    
    def __init__(self):
        self.enabled = os.getenv("LOCAL_LLM_ENABLED", "false").lower() == "true"
        self.endpoint = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:11434")
        self.model = os.getenv("LOCAL_LLM_MODEL", "llama3.2:3b")
        self.timeout = int(os.getenv("LOCAL_LLM_TIMEOUT", "30"))
        self.max_tokens = int(os.getenv("LOCAL_LLM_MAX_TOKENS", "2000"))
        
        # Cleanup endpoint URL
        if not self.endpoint.startswith(('http://', 'https://')):
            self.endpoint = f"http://{self.endpoint}"
        if not self.endpoint.endswith('/'):
            self.endpoint = f"{self.endpoint}/"
            
        self.chat_url = f"{self.endpoint}api/chat"
        self.generate_url = f"{self.endpoint}api/generate"
        
        logger.info(f"🤖 Local LLM Service initialized - Enabled: {self.enabled}")
        if self.enabled:
            logger.info(f"📡 Endpoint: {self.endpoint}")
            logger.info(f"🧠 Model: {self.model}")
    
    async def is_available(self) -> bool:
        """Check if local LLM service is available"""
        if not self.enabled:
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.endpoint}api/tags",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Check if our model is available
                        models = [model['name'] for model in data.get('models', [])]
                        is_model_available = self.model in models
                        logger.info(f"🔍 Local LLM available: {response.status == 200}, Model '{self.model}' available: {is_model_available}")
                        return is_model_available
                    return False
        except Exception as e:
            logger.warning(f"⚠️ Local LLM not available: {str(e)}")
            return False
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate chat completion using local LLM
        """
        if not self.enabled:
            raise Exception("Local LLM not enabled")
        
        try:
            # Prepare messages for Ollama format
            ollama_messages = []
            for msg in messages:
                ollama_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            payload = {
                "model": self.model,
                "messages": ollama_messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens or self.max_tokens,
                    "top_p": 0.9,
                    "stop": ["</s>", "[INST]", "[/INST]"]
                }
            }
            
            logger.info(f"🚀 Sending request to local LLM: {self.model}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.chat_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        assistant_content = result.get('message', {}).get('content', '')
                        
                        # Calculate approximate token counts (rough estimation)
                        prompt_tokens = sum(len(msg['content'].split()) for msg in messages)
                        completion_tokens = len(assistant_content.split())
                        
                        logger.info(f"✅ Local LLM response received ({completion_tokens} tokens)")
                        
                        return {
                            "response": assistant_content,
                            "model": self.model,
                            "usage": {
                                "prompt_tokens": prompt_tokens,
                                "completion_tokens": completion_tokens,
                                "total_tokens": prompt_tokens + completion_tokens
                            },
                            "provider": "local_llm"
                        }
                    else:
                        error_text = await response.text()
                        raise Exception(f"Local LLM request failed: {response.status} - {error_text}")
                        
        except asyncio.TimeoutError:
            logger.error(f"❌ Local LLM timeout after {self.timeout}s")
            raise Exception(f"Local LLM request timed out after {self.timeout}s")
        except Exception as e:
            logger.error(f"❌ Local LLM request failed: {str(e)}")
            raise Exception(f"Local LLM error: {str(e)}")
    
    async def simple_generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Simple text generation using local LLM
        """
        if not self.enabled:
            raise Exception("Local LLM not enabled")
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens or self.max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.generate_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return result.get('response', '')
                    else:
                        error_text = await response.text()
                        raise Exception(f"Generate request failed: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"❌ Local LLM generate failed: {str(e)}")
            raise Exception(f"Local LLM generate error: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get local LLM service status"""
        return {
            "enabled": self.enabled,
            "endpoint": self.endpoint,
            "model": self.model,
            "timeout": self.timeout,
            "max_tokens": self.max_tokens
        }

# Global instance
local_llm_service = LocalLLMService()