# Add to your project root: rate_limiter.py
import asyncio
from datetime import datetime, timedelta
from collections import deque

class GeminiRateLimiter:
    def __init__(self, max_calls=4, time_window=60):
        """
        max_calls=4 to stay safely under 5/min limit
        time_window=60 seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.call_times = deque(maxlen=max_calls)
    
    async def acquire(self):
        """Wait if necessary before making API call"""
        now = datetime.now()
        
        # If we have max_calls in the window, wait
        if len(self.call_times) >= self.max_calls:
            oldest_call = self.call_times[0]
            time_since_oldest = (now - oldest_call).total_seconds()
            
            if time_since_oldest < self.time_window:
                wait_time = self.time_window - time_since_oldest + 1
                print(f"⏳ Rate limit: waiting {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
        
        self.call_times.append(datetime.now())

# Global rate limiter
rate_limiter = GeminiRateLimiter(max_calls=4, time_window=60)