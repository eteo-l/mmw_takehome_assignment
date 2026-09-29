# Design and implement an in-memory rate limiter with one method,
# `allow(client_id) -> bool`, returning whether a request from that client
# is allowed under a limit of N requests per rolling W-second window.
# Assume a single process -- no distributed or multi-server concerns.

# Build it, then structure it so a second limiting strategy (for example,
# a fixed window instead of a rolling one) could be added later without
# changing how callers use `allow()`. You don't need to implement the second
# strategy -- but explain in your write-up how a second strategy would plug in.

import time
from collections import deque
from typing import Protocol, Callable


class RateLimiter(Protocol):
    """Protocol for rate limiting strategies."""

    def allow(self, client_id: str) -> bool:
        """Check if a request from client_id is allowed."""
        ...


class SlidingWindowRateLimiter:
    """Rate limiter using sliding window with a deque of timestamps per client."""

    def __init__(self, max_requests: int, window_seconds: float, clock: Callable[[], float] = time.monotonic):
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum number of requests allowed per window (must be > 0)
            window_seconds: Size of the rolling window in seconds (must be > 0)
            clock: Function that returns current time (defaults to time.monotonic)

        Raises:
            ValueError: If max_requests or window_seconds is <= 0
        """
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than 0")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than 0")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clock = clock
        self.clients: dict[str, deque[float]] = {}

    def allow(self, client_id: str) -> bool:
        """
        Check if a request from client_id is allowed.

        A request is allowed if fewer than max_requests have been made
        in the last window_seconds (exclusive of exactly window_seconds ago).
        Denied requests are not recorded.

        Args:
            client_id: Identifier for the client making the request

        Returns:
            True if the request is allowed, False otherwise
        """
        now = self.clock()

        # Get or create the client's request log
        if client_id not in self.clients:
            self.clients[client_id] = deque()

        timestamps = self.clients[client_id]

        # Remove requests that are outside the window (>= window_seconds old)
        cutoff = now - self.window_seconds
        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

        # Check if the client has exceeded the limit
        if len(timestamps) >= self.max_requests:
            return False

        # Request is allowed - record it
        timestamps.append(now)

        # Clean up empty deques
        if not timestamps:
            del self.clients[client_id]

        return True
