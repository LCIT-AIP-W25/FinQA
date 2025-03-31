import random
import time
import threading
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class KeyStatus:
    key: str
    last_used: float = 0
    error_count: int = 0
    success_count: int = 0
    disabled_until: Optional[float] = None

class EnhancedGroqKeyManager:
    def __init__(self):
        self.rag_keys: Dict[str, KeyStatus] = {}
        self.sql_keys: Dict[str, KeyStatus] = {}
        self.summarize_keys: Dict[str, KeyStatus] = {}
        self._lock = threading.Lock()
        self.error_threshold = 3  # Disable key after 3 consecutive errors
        self.cooldown_period = 300  # 5 minutes cooldown for failed keys
    
    def initialize_keys(self, rag_keys: List[str], sql_keys: List[str], summarize_keys: List[str]):
        """Initialize the key manager with all available keys"""
        with self._lock:
            self.rag_keys = {key: KeyStatus(key) for key in rag_keys}
            self.sql_keys = {key: KeyStatus(key) for key in sql_keys}
            self.summarize_keys = {key: KeyStatus(key) for key in summarize_keys}
    
    def _get_random_available_key(self, key_pool: Dict[str, KeyStatus]) -> str:
        """Get a random available key from the specified pool"""
        now = time.time()
        available_keys = [
            k for k, status in key_pool.items()
            if status.disabled_until is None or status.disabled_until < now
        ]
        
        if not available_keys:
            raise ValueError("No available keys in this category")
            
        selected_key = random.choice(available_keys)
        key_pool[selected_key].last_used = now
        return selected_key
    
    def _mark_key_result(self, key_pool: Dict[str, KeyStatus], key: str, success: bool):
        """Record whether a key usage was successful or not"""
        with self._lock:
            if key not in key_pool:
                return
            
            status = key_pool[key]
            if success:
                status.success_count += 1
                status.error_count = 0
            else:
                status.error_count += 1
                status.success_count = 0
                
                if status.error_count >= self.error_threshold:
                    status.disabled_until = time.time() + self.cooldown_period
    
    def get_rag_key(self) -> str:
        """Get a random available RAG key"""
        with self._lock:
            return self._get_random_available_key(self.rag_keys)
    
    def get_sql_key(self) -> str:
        """Get a random available SQL key"""
        with self._lock:
            return self._get_random_available_key(self.sql_keys)
    
    def get_summarize_key(self) -> str:
        """Get a random available summarize key"""
        with self._lock:
            return self._get_random_available_key(self.summarize_keys)
    
    def mark_rag_key_result(self, key: str, success: bool):
        """Record RAG key usage result"""
        self._mark_key_result(self.rag_keys, key, success)
    
    def mark_sql_key_result(self, key: str, success: bool):
        """Record SQL key usage result"""
        self._mark_key_result(self.sql_keys, key, success)
    
    def mark_summarize_key_result(self, key: str, success: bool):
        """Record summarize key usage result"""
        self._mark_key_result(self.summarize_keys, key, success)
    
    def get_usage_stats(self) -> Dict[str, Dict]:
        """Get usage statistics for all keys"""
        with self._lock:
            return {
                "rag_keys": {k: vars(v) for k, v in self.rag_keys.items()},
                "sql_keys": {k: vars(v) for k, v in self.sql_keys.items()},
                "summarize_keys": {k: vars(v) for k, v in self.summarize_keys.items()}
            }

# Global instance
key_manager = EnhancedGroqKeyManager()