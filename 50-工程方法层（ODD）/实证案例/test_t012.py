import pytest
import time
import threading
from rate_limiter import (
    FixedWindowRateLimiter,
    SlidingWindowRateLimiter,
    ConcurrencyLimiter,
    AccessControl,
    ComprehensiveRateLimiter,
    RateLimitContext,
    QPSExceededError,
    ConcurrencyExceededError,
    BlacklistedError,
)


class TestFixedWindowRateLimiter:
    def test_basic_limiting(self):
        limiter = FixedWindowRateLimiter(qps=3, window=1.0)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
    
    def test_window_reset(self):
        limiter = FixedWindowRateLimiter(qps=2, window=0.1)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
        time.sleep(0.15)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
    
    def test_multiple_identifiers(self):
        limiter = FixedWindowRateLimiter(qps=2, window=1.0)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
        assert limiter.allow("user2") is True
        assert limiter.allow("user2") is True
    
    def test_reset(self):
        limiter = FixedWindowRateLimiter(qps=2, window=1.0)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
        limiter.reset("user1")
        assert limiter.allow("user1") is True


class TestSlidingWindowRateLimiter:
    def test_basic_limiting(self):
        limiter = SlidingWindowRateLimiter(qps=3, window=1.0)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
    
    def test_sliding_behavior(self):
        limiter = SlidingWindowRateLimiter(qps=2, window=0.2)
        assert limiter.allow("user1") is True
        time.sleep(0.05)
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
        time.sleep(0.16)
        assert limiter.allow("user1") is True
    
    def test_multiple_identifiers(self):
        limiter = SlidingWindowRateLimiter(qps=2, window=1.0)
        assert limiter.allow("user1") is True
        assert limiter.allow("user2") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user2") is True
        assert limiter.allow("user1") is False
        assert limiter.allow("user2") is False


class TestConcurrencyLimiter:
    def test_basic_concurrency(self):
        limiter = ConcurrencyLimiter(max_concurrent=2)
        assert limiter.acquire("user1") is True
        assert limiter.acquire("user1") is True
        assert limiter.acquire("user1") is False
        limiter.release("user1")
        assert limiter.acquire("user1") is True
    
    def test_multiple_identifiers(self):
        limiter = ConcurrencyLimiter(max_concurrent=2)
        assert limiter.acquire("user1") is True
        assert limiter.acquire("user2") is True
        assert limiter.acquire("user1") is True
        assert limiter.acquire("user2") is True
        assert limiter.acquire("user1") is False
        assert limiter.acquire("user2") is False


class TestAccessControl:
    def test_no_lists(self):
        ac = AccessControl()
        assert ac.is_allowed("user1") is True
        assert ac.is_allowed("user2") is True
    
    def test_blacklist(self):
        ac = AccessControl()
        ac.add_to_blacklist("user1")
        assert ac.is_allowed("user1") is False
        assert ac.is_allowed("user2") is True
    
    def test_whitelist(self):
        ac = AccessControl()
        ac.add_to_whitelist("user1")
        assert ac.is_allowed("user1") is True
        assert ac.is_allowed("user2") is False
    
    def test_blacklist_priority(self):
        ac = AccessControl()
        ac.add_to_whitelist("user1")
        ac.add_to_blacklist("user1")
        assert ac.is_allowed("user1") is False
    
    def test_remove(self):
        ac = AccessControl()
        ac.add_to_blacklist("user1")
        assert ac.is_allowed("user1") is False
        ac.remove_from_blacklist("user1")
        assert ac.is_allowed("user1") is True


class TestComprehensiveRateLimiter:
    def test_qps_limiting(self):
        limiter = ComprehensiveRateLimiter(qps=3, window=1.0, algorithm="sliding")
        limiter.check("user1")
        limiter.check("user1")
        limiter.check("user1")
        with pytest.raises(QPSExceededError) as exc_info:
            limiter.check("user1")
        assert exc_info.value.identifier == "user1"
        assert exc_info.value.limit == 3
    
    def test_concurrency_limiting(self):
        limiter = ComprehensiveRateLimiter(qps=100, window=1.0, algorithm="sliding", max_concurrent=2)
        limiter.check("user1")
        limiter.check("user1")
        with pytest.raises(ConcurrencyExceededError) as exc_info:
            limiter.check("user1")
        assert exc_info.value.identifier == "user1"
        limiter.release("user1")
        limiter.check("user1")
    
    def test_blacklist(self):
        limiter = ComprehensiveRateLimiter(qps=100, window=1.0)
        limiter.add_to_blacklist("user1")
        with pytest.raises(BlacklistedError) as exc_info:
            limiter.check("user1")
        assert exc_info.value.identifier == "user1"
    
    def test_whitelist(self):
        limiter = ComprehensiveRateLimiter(qps=100, window=1.0)
        limiter.add_to_whitelist("user1")
        limiter.check("user1")
        with pytest.raises(BlacklistedError):
            limiter.check("user2")
    
    def test_context_manager(self):
        limiter = ComprehensiveRateLimiter(qps=100, window=1.0, max_concurrent=1)
        with RateLimitContext(limiter, "user1"):
            with pytest.raises(ConcurrencyExceededError):
                limiter.check("user1")
        limiter.check("user1")
    
    def test_fixed_window_algorithm(self):
        limiter = ComprehensiveRateLimiter(qps=2, window=0.1, algorithm="fixed")
        limiter.check("user1")
        limiter.check("user1")
        with pytest.raises(QPSExceededError):
            limiter.check("user1")
        time.sleep(0.15)
        limiter.check("user1")
