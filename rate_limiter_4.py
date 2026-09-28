# Design and implement an in-memory rate limiter with one method, 
# `allow(client_id) -> bool`, returning whether a request from that client 
# is allowed under a limit of N requests per rolling W-second window. 
# Assume a single process -- no distributed or multi-server concerns.

# Build it, then structure it so a second limiting strategy (for example, 
# a fixed window instead of a rolling one) could be added later without 
# changing how callers use `allow()`. You don't need to implement the second 
# strategy -- but explain in your write-up how a second strategy would plug in.
