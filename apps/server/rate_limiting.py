"""
Rate limiting functionality for API endpoints.
"""

import os
import time
from collections import defaultdict, deque
from datetime import datetime
from fastapi import HTTPException, Depends
from typing import Dict

# Rate Limiting Configuration
RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "5"))  # Max calls per window
RATE_LIMIT_WINDOW_MINUTES = int(os.getenv("RATE_LIMIT_WINDOW_MINUTES", "5"))  # Window in minutes
RATE_LIMIT_WINDOW_SECONDS = RATE_LIMIT_WINDOW_MINUTES * 60

# Rate limiting store - tracks call timestamps per token
RATE_LIMIT_STORE = defaultdict(lambda: deque())

DEBUG_LOGS = os.getenv("DEBUG_LOGS", "false").lower() == "true"


def cleanup_rate_limit_store():
    """Clean up old entries from rate limit store to prevent memory growth"""
    current_time = time.time()
    cutoff_time = current_time - RATE_LIMIT_WINDOW_SECONDS
    
    # Clean up old entries for all tokens
    for token in list(RATE_LIMIT_STORE.keys()):
        timestamps = RATE_LIMIT_STORE[token]
        # Remove timestamps older than the window
        while timestamps and timestamps[0] < cutoff_time:
            timestamps.popleft()
        
        # If no timestamps left, remove the token entry
        if not timestamps:
            del RATE_LIMIT_STORE[token]
    
    if DEBUG_LOGS:
        print(f"🧹 Rate limit cleanup completed. Active tokens: {len(RATE_LIMIT_STORE)}")


def check_rate_limit(token: str) -> Dict:
    """
    Check if token is within rate limits
    Returns: {'allowed': bool, 'remaining': int, 'reset_time': float}
    """
    current_time = time.time()
    cutoff_time = current_time - RATE_LIMIT_WINDOW_SECONDS
    
    # Get or create timestamps for this token
    timestamps = RATE_LIMIT_STORE[token]
    
    # Remove old timestamps outside the window
    while timestamps and timestamps[0] < cutoff_time:
        timestamps.popleft()
    
    # Check if we're within the limit
    call_count = len(timestamps)
    allowed = call_count < RATE_LIMIT_CALLS
    
    if allowed:
        # Add current timestamp
        timestamps.append(current_time)
        call_count += 1
    
    # Calculate reset time (when the oldest call in window will expire)
    reset_time = timestamps[0] + RATE_LIMIT_WINDOW_SECONDS if timestamps else current_time
    remaining = max(0, RATE_LIMIT_CALLS - call_count)
    
    return {
        'allowed': allowed,
        'remaining': remaining,
        'reset_time': reset_time,
        'current_count': call_count,
        'limit': RATE_LIMIT_CALLS,
        'window_minutes': RATE_LIMIT_WINDOW_MINUTES
    }


def rate_limit_dependency(current_user: Dict = Depends(lambda: {})):
    """Dependency to check rate limits for authenticated users"""
    # Use session_id as the rate limiting key (unique per token)
    token_key = current_user.get("session_id", "unknown")
    
    # Clean up old entries periodically (every 10th call to avoid overhead)
    if len(RATE_LIMIT_STORE) % 10 == 0:
        cleanup_rate_limit_store()
    
    # Check rate limit
    rate_info = check_rate_limit(token_key)
    
    if not rate_info['allowed']:
        reset_time_utc = datetime.fromtimestamp(rate_info['reset_time'])
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "message": f"Too many calls. Limit: {rate_info['limit']} calls per {rate_info['window_minutes']} minutes",
                "remaining": rate_info['remaining'],
                "reset_time": reset_time_utc.isoformat(),
                "current_count": rate_info['current_count']
            }
        )
    
    return current_user


def get_rate_limit_status(token: str) -> Dict:
    """Get current rate limit status for a token without incrementing"""
    # Clean up old entries first
    cleanup_rate_limit_store()
    
    # Get current rate limit info without incrementing
    current_time = time.time()
    cutoff_time = current_time - RATE_LIMIT_WINDOW_SECONDS
    
    timestamps = RATE_LIMIT_STORE[token]
    # Remove old timestamps for accurate count
    while timestamps and timestamps[0] < cutoff_time:
        timestamps.popleft()
    
    call_count = len(timestamps)
    remaining = max(0, RATE_LIMIT_CALLS - call_count)
    reset_time = timestamps[0] + RATE_LIMIT_WINDOW_SECONDS if timestamps else current_time
    
    return {
        "limit": RATE_LIMIT_CALLS,
        "window_minutes": RATE_LIMIT_WINDOW_MINUTES,
        "current_count": call_count,
        "remaining": remaining,
        "reset_time": datetime.fromtimestamp(reset_time).isoformat(),
        "can_make_call": call_count < RATE_LIMIT_CALLS
    }


def get_rate_limit_config() -> Dict:
    """Get rate limiting configuration for debugging/monitoring"""
    return {
        "calls_per_window": RATE_LIMIT_CALLS,
        "window_minutes": RATE_LIMIT_WINDOW_MINUTES,
        "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
        "active_tokens": len(RATE_LIMIT_STORE)
    }
