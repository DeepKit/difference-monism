import pytest
import sys
sys.path.insert(0, '.')
from rate_limiter_v2 import RequestRateLimiter

def test_ratelimiter_init():
    rl = RequestRateLimiter(max_requests=10, window_seconds=60)
    assert rl is not None

def test_ratelimiter_allow():
    rl = RequestRateLimiter(max_requests=10, window_seconds=60)
    result = rl.is_allowed("user1")
    assert result == True