from groq import Groq
from groq_key_manager import key_manager
import time
from typing import Optional, Tuple

class GroqWrapper:
    @staticmethod
    def make_rag_request(*args, **kwargs) -> Tuple[Optional[dict], Optional[str]]:
        """Make a RAG request with error handling and key rotation"""
        return GroqWrapper._make_request(
            key_manager.get_rag_key,
            key_manager.mark_rag_key_result,
            *args, **kwargs
        )
    
    @staticmethod
    def make_sql_request(*args, **kwargs) -> Tuple[Optional[dict], Optional[str]]:
        """Make a SQL request with error handling and key rotation"""
        return GroqWrapper._make_request(
            key_manager.get_sql_key,
            key_manager.mark_sql_key_result,
            *args, **kwargs
        )
    
    @staticmethod
    def make_summarize_request(*args, **kwargs) -> Tuple[Optional[dict], Optional[str]]:
        """Make a summarize request with error handling and key rotation"""
        return GroqWrapper._make_request(
            key_manager.get_summarize_key,
            key_manager.mark_summarize_key_result,
            *args, **kwargs
        )
    
    @staticmethod
    def _make_request(key_getter, result_marker, *args, **kwargs):
        """Generic request handler with retry logic"""
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            key = key_getter()
            try:
                print(f"Using API Key: {key[-6]}... (Attempt {attempt + 1}/{max_retries})")
                client = Groq(api_key=key)
                start_time = time.time()
                response = client.chat.completions.create(*args, **kwargs)
                latency = time.time() - start_time
                
                # Record successful usage
                result_marker(key, True)
                
                # Add latency information to response
                if hasattr(response, '__dict__'):
                    response.__dict__['_metadata'] = {
                        'api_key': key[-6:],  # Last 6 chars for identification
                        'latency': latency,
                        'attempt': attempt + 1
                    }
        
                
                return response, None
                
            except Exception as e:
                last_error = str(e)
                result_marker(key, False)
                
                print(f"❌ Key {key[-6:]} failed: {str(e)[:100]}...")
                # Exponential backoff
                time.sleep(2 ** attempt)
        
        return None, last_error