# Tests for problem 4: rate limiter
import pytest
from rate_limiter_4 import SlidingWindowRateLimiter


class FakeClock:
    """Fake clock for testing without sleep."""

    def __init__(self, start_time: float = 0.0):
        self.current_time = start_time

    def __call__(self) -> float:
        return self.current_time

    def advance(self, seconds: float) -> None:
        """Advance the clock by the given number of seconds."""
        self.current_time += seconds

    def set(self, time: float) -> None:
        """Set the clock to a specific time."""
        self.current_time = time


class TestSlidingWindowRateLimiter:
    """Test suite for SlidingWindowRateLimiter."""

    def test_validation_max_requests_zero(self):
        """Test that max_requests <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="max_requests must be greater than 0"):
            SlidingWindowRateLimiter(0, 10)

    def test_validation_max_requests_negative(self):
        """Test that negative max_requests raises ValueError."""
        with pytest.raises(ValueError, match="max_requests must be greater than 0"):
            SlidingWindowRateLimiter(-5, 10)

    def test_validation_window_seconds_zero(self):
        """Test that window_seconds <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="window_seconds must be greater than 0"):
            SlidingWindowRateLimiter(5, 0)

    def test_validation_window_seconds_negative(self):
        """Test that negative window_seconds raises ValueError."""
        with pytest.raises(ValueError, match="window_seconds must be greater than 0"):
            SlidingWindowRateLimiter(5, -10)

    def test_first_request_allowed(self):
        """Test that the first request is always allowed."""
        clock = FakeClock()
        limiter = SlidingWindowRateLimiter(5, 10, clock=clock)
        assert limiter.allow("client1") is True

    def test_within_limit_all_allowed(self):
        """Test that requests within limit are all allowed."""
        clock = FakeClock()
        limiter = SlidingWindowRateLimiter(5, 10, clock=clock)

        for i in range(5):
            assert limiter.allow("client1") is True

    def test_sixth_request_denied(self):
        """Test that 6th request in a 5-per-window limit is denied."""
        clock = FakeClock()
        limiter = SlidingWindowRateLimiter(5, 10, clock=clock)

        # First 5 requests allowed
        for i in range(5):
            assert limiter.allow("client1") is True

        # 6th request denied
        assert limiter.allow("client1") is False

    def test_exact_window_boundary(self):
        """Test that a request exactly W seconds old is outside the window."""
        clock = FakeClock(0.0)
        limiter = SlidingWindowRateLimiter(5, 10, clock=clock)

        # Make 5 requests at time 0
        for i in range(5):
            assert limiter.allow("client1") is True

        # At time 9.999, oldest request is 9.999 seconds old - still in window
        clock.set(9.999)
        assert limiter.allow("client1") is False  # Still blocked

        # At time 10.0, oldest request is exactly 10 seconds old - outside window
        clock.set(10.0)
        assert limiter.allow("client1") is True  # Now allowed

    def test_denied_requests_not_recorded(self):
        """Test that denied requests don't extend the blocking period."""
        clock = FakeClock(0.0)
        limiter = SlidingWindowRateLimiter(5, 10, clock=clock)

        # Fill up the limit at time 0
        for i in range(5):
            assert limiter.allow("client1") is True

        # Denied at time 5
        clock.set(5.0)
        assert limiter.allow("client1") is False

        # Advance to time 10 - oldest request (from time 0) should be outside window
        clock.set(10.0)
        assert limiter.allow("client1") is True  # Should be allowed

        # If denied request at time 5 was recorded, we'd still be blocked
        # But since it wasn't, we're only at 5 requests in window again
        for i in range(4):
            assert limiter.allow("client1") is True

        # Now we should be blocked again
        assert limiter.allow("client1") is False

    def test_clients_are_independent(self):
        """Test that different clients have independent rate limits."""
        clock = FakeClock()
        limiter = SlidingWindowRateLimiter(2, 10, clock=clock)

        # Client 1 uses up its limit
        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is False

        # Client 2 should still have its full limit
        assert limiter.allow("client2") is True
        assert limiter.allow("client2") is True
        assert limiter.allow("client2") is False

        # Client 3 should also have its full limit
        assert limiter.allow("client3") is True
        assert limiter.allow("client3") is True
        assert limiter.allow("client3") is False

    def test_rolling_window_behavior(self):
        """Test that the window rolls correctly as time advances."""
        clock = FakeClock(0.0)
        limiter = SlidingWindowRateLimiter(3, 10, clock=clock)

        # Time 0: 3 requests
        assert limiter.allow("client1") is True
        clock.advance(1)
        assert limiter.allow("client1") is True
        clock.advance(1)
        assert limiter.allow("client1") is True

        # Time 2: limit reached
        assert limiter.allow("client1") is False

        # Time 10: first request (from time 0) falls out of window
        clock.set(10.0)
        assert limiter.allow("client1") is True  # Allowed

        # Time 11: second request (from time 1) falls out
        clock.set(11.0)
        assert limiter.allow("client1") is True  # Allowed

        # Now at limit again
        assert limiter.allow("client1") is False

    def test_empty_deque_cleanup(self):
        """Test that clients with empty deques are removed."""
        clock = FakeClock(0.0)
        limiter = SlidingWindowRateLimiter(2, 10, clock=clock)

        # Make requests
        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is True

        # Client should be in the dict
        assert "client1" in limiter.clients

        # Advance past the window
        clock.set(10.1)

        # Next allow() call should clean up old timestamps
        assert limiter.allow("client1") is True

        # Client should still be in dict (has 1 request now)
        assert "client1" in limiter.clients

        # Advance past this request
        clock.set(20.2)

        # This should clean up and then add a new request
        assert limiter.allow("client1") is True
        assert "client1" in limiter.clients

    def test_single_request_limit(self):
        """Test edge case with max_requests=1."""
        clock = FakeClock(0.0)
        limiter = SlidingWindowRateLimiter(1, 5, clock=clock)

        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is False

        clock.set(5.0)
        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is False

    def test_fractional_window(self):
        """Test that fractional window seconds work correctly."""
        clock = FakeClock(0.0)
        limiter = SlidingWindowRateLimiter(2, 0.5, clock=clock)

        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is True
        assert limiter.allow("client1") is False

        clock.set(0.5)
        assert limiter.allow("client1") is True
