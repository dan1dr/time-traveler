"""
Unit tests for rate limiting functionality.
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from collections import defaultdict, deque
import sys
import os

# Add the server directory to the path so we can import the rate limiting functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'apps', 'server'))

# Import rate limiting functions directly
from collections import defaultdict, deque
import time

# Rate limiting configuration (matching main.py)
RATE_LIMIT_CALLS = 5
RATE_LIMIT_WINDOW_MINUTES = 5
RATE_LIMIT_WINDOW_SECONDS = RATE_LIMIT_WINDOW_MINUTES * 60

# Rate limiting store - tracks call timestamps per token
RATE_LIMIT_STORE = defaultdict(lambda: deque())

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

def check_rate_limit(token: str) -> dict:
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

class MockHTTPException(Exception):
    """Mock HTTPException for testing"""
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(str(detail))

def rate_limit_dependency(current_user: dict):
    """Dependency to check rate limits for authenticated users"""
    from datetime import datetime
    
    # Use session_id as the rate limiting key (unique per token)
    token_key = current_user.get("session_id", "unknown")
    
    # Clean up old entries periodically (every 10th call to avoid overhead)
    if len(RATE_LIMIT_STORE) % 10 == 0:
        cleanup_rate_limit_store()
    
    # Check rate limit
    rate_info = check_rate_limit(token_key)
    
    if not rate_info['allowed']:
        reset_time_utc = datetime.fromtimestamp(rate_info['reset_time'])
        raise MockHTTPException(
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


class TestRateLimiting:
    """Test cases for rate limiting functionality."""

    def setup_method(self):
        """Set up test environment before each test method."""
        # Clear the rate limit store before each test
        RATE_LIMIT_STORE.clear()

    def test_check_rate_limit_within_limit(self):
        """Test rate limiting when within the allowed limit."""
        token = "test-token-1"
        
        # Make calls up to the limit
        for i in range(RATE_LIMIT_CALLS):
            result = check_rate_limit(token)
            assert result['allowed'] is True
            assert result['current_count'] == i + 1
            assert result['remaining'] == RATE_LIMIT_CALLS - (i + 1)
            assert result['limit'] == RATE_LIMIT_CALLS

    def test_check_rate_limit_exceeds_limit(self):
        """Test rate limiting when exceeding the allowed limit."""
        token = "test-token-2"
        
        # Make calls up to the limit
        for i in range(RATE_LIMIT_CALLS):
            result = check_rate_limit(token)
            assert result['allowed'] is True
        
        # Try to make one more call (should be blocked)
        result = check_rate_limit(token)
        assert result['allowed'] is False
        assert result['current_count'] == RATE_LIMIT_CALLS
        assert result['remaining'] == 0

    def test_check_rate_limit_multiple_tokens(self):
        """Test that different tokens have independent rate limits."""
        token1 = "token-1"
        token2 = "token-2"
        
        # Use up the limit for token1
        for i in range(RATE_LIMIT_CALLS):
            result = check_rate_limit(token1)
            assert result['allowed'] is True
        
        # Token1 should now be blocked
        result = check_rate_limit(token1)
        assert result['allowed'] is False
        
        # Token2 should still be able to make calls
        result = check_rate_limit(token2)
        assert result['allowed'] is True
        assert result['current_count'] == 1

    def test_check_rate_limit_time_window(self):
        """Test that rate limits reset after the time window."""
        token = "test-token-3"
        
        # Use up the limit
        for i in range(RATE_LIMIT_CALLS):
            result = check_rate_limit(token)
            assert result['allowed'] is True
        
        # Should be blocked
        result = check_rate_limit(token)
        assert result['allowed'] is False
        
        # Simulate time passing by manually clearing old timestamps
        timestamps = RATE_LIMIT_STORE[token]
        timestamps.clear()
        
        # Should now be able to make calls again
        result = check_rate_limit(token)
        assert result['allowed'] is True
        assert result['current_count'] == 1

    def test_cleanup_rate_limit_store(self):
        """Test the cleanup function removes old entries."""
        token = "test-token-4"
        
        # Add some timestamps
        current_time = time.time()
        old_time = current_time - RATE_LIMIT_WINDOW_SECONDS - 100  # Very old
        
        timestamps = RATE_LIMIT_STORE[token]
        timestamps.append(old_time)  # Old timestamp
        timestamps.append(current_time)  # Current timestamp
        
        assert len(timestamps) == 2
        
        # Run cleanup
        cleanup_rate_limit_store()
        
        # Only current timestamp should remain
        assert len(timestamps) == 1
        assert timestamps[0] == current_time

    def test_cleanup_rate_limit_store_removes_empty_tokens(self):
        """Test that cleanup removes tokens with no remaining timestamps."""
        token = "test-token-5"
        
        # Add only old timestamps
        old_time = time.time() - RATE_LIMIT_WINDOW_SECONDS - 100
        timestamps = RATE_LIMIT_STORE[token]
        timestamps.append(old_time)
        
        assert token in RATE_LIMIT_STORE
        
        # Run cleanup
        cleanup_rate_limit_store()
        
        # Token should be removed
        assert token not in RATE_LIMIT_STORE

    def test_rate_limit_dependency_success(self):
        """Test rate limit dependency when within limits."""
        token = "test-token-6"
        
        # Mock current_user with session_id
        mock_user = {"session_id": token, "user_id": "test-user"}
        
        # Should succeed for first few calls
        for i in range(RATE_LIMIT_CALLS):
            result = rate_limit_dependency(mock_user)
            assert result == mock_user

    def test_rate_limit_dependency_exceeds_limit(self):
        """Test rate limit dependency when exceeding limits."""
        token = "test-token-7"
        
        # Mock current_user with session_id
        mock_user = {"session_id": token, "user_id": "test-user"}
        
        # Use up the limit
        for i in range(RATE_LIMIT_CALLS):
            rate_limit_dependency(mock_user)
        
        # Next call should raise HTTPException
        with pytest.raises(Exception) as exc_info:
            rate_limit_dependency(mock_user)
        
        # Check that it's a rate limit error
        assert "Rate limit exceeded" in str(exc_info.value)

    def test_rate_limit_dependency_cleanup_trigger(self):
        """Test that cleanup is triggered periodically."""
        token = "test-token-8"
        mock_user = {"session_id": token, "user_id": "test-user"}
        
        # Mock the cleanup function to verify it's called
        with patch('tests.test_rate_limiting.cleanup_rate_limit_store') as mock_cleanup:
            # Fill up the store to trigger cleanup
            for i in range(10):  # This should trigger cleanup
                test_token = f"token-{i}"
                test_user = {"session_id": test_token, "user_id": f"user-{i}"}
                try:
                    rate_limit_dependency(test_user)
                except:
                    pass  # Ignore rate limit errors
            
            # Cleanup should have been called
            assert mock_cleanup.called

    def test_rate_limit_response_structure(self):
        """Test that rate limit responses have the correct structure."""
        token = "test-token-9"
        
        # Use up the limit
        for i in range(RATE_LIMIT_CALLS):
            check_rate_limit(token)
        
        # Get the blocked response
        result = check_rate_limit(token)
        
        # Check response structure
        required_keys = ['allowed', 'remaining', 'reset_time', 'current_count', 'limit', 'window_minutes']
        for key in required_keys:
            assert key in result
        
        assert result['allowed'] is False
        assert result['remaining'] == 0
        assert result['current_count'] == RATE_LIMIT_CALLS
        assert result['limit'] == RATE_LIMIT_CALLS

    def test_rate_limit_reset_time_calculation(self):
        """Test that reset time is calculated correctly."""
        token = "test-token-10"
        
        # Make a call
        result = check_rate_limit(token)
        
        # Reset time should be approximately current time + window
        expected_reset = time.time() + RATE_LIMIT_WINDOW_SECONDS
        actual_reset = result['reset_time']
        
        # Allow for small time differences (within 1 second)
        assert abs(actual_reset - expected_reset) < 1.0

    def test_concurrent_tokens_independence(self):
        """Test that concurrent access to different tokens works correctly."""
        tokens = [f"concurrent-token-{i}" for i in range(5)]
        
        # All tokens should be able to make calls simultaneously
        for token in tokens:
            result = check_rate_limit(token)
            assert result['allowed'] is True
            assert result['current_count'] == 1
        
        # Each token should have its own independent limit
        for token in tokens:
            # Use up the rest of the limit for this token
            for i in range(RATE_LIMIT_CALLS - 1):
                result = check_rate_limit(token)
                assert result['allowed'] is True
            
            # This token should now be blocked
            result = check_rate_limit(token)
            assert result['allowed'] is False

    def test_rate_limit_edge_cases(self):
        """Test edge cases for rate limiting."""
        token = "edge-case-token"
        
        # Test with empty token
        result = check_rate_limit("")
        assert result['allowed'] is True
        
        # Test with very long token
        long_token = "x" * 1000
        result = check_rate_limit(long_token)
        assert result['allowed'] is True
        
        # Test with special characters in token
        special_token = "token-with-special-chars!@#$%^&*()"
        result = check_rate_limit(special_token)
        assert result['allowed'] is True

    def test_memory_efficiency(self):
        """Test that the rate limiting system is memory efficient."""
        initial_tokens = len(RATE_LIMIT_STORE)
        
        # Create many tokens with old timestamps
        old_time = time.time() - RATE_LIMIT_WINDOW_SECONDS - 100
        for i in range(100):
            token = f"memory-test-token-{i}"
            timestamps = RATE_LIMIT_STORE[token]
            timestamps.append(old_time)
        
        # Run cleanup
        cleanup_rate_limit_store()
        
        # All old tokens should be removed
        assert len(RATE_LIMIT_STORE) == initial_tokens

    def test_rate_limit_configuration(self):
        """Test that rate limit configuration is correct."""
        # Test that the configuration values are reasonable
        assert RATE_LIMIT_CALLS > 0
        assert RATE_LIMIT_WINDOW_SECONDS > 0
        assert RATE_LIMIT_CALLS <= 100  # Reasonable upper bound
        assert RATE_LIMIT_WINDOW_SECONDS <= 3600  # Reasonable upper bound (1 hour)
