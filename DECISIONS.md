# DECISIONS.md

## 1. Why I chose this ingestion approach

I considered a simple scraper that fetches once and fails loudly if anything goes wrong,
but rejected that — a real pipeline needs to handle temporary problems like an empty
response, rate limiting, or a source changing shape overnight.

Instead I added a fetch layer with retries and exponential backoff (up to 3 attempts,
increasing wait time), plus a `/status` endpoint showing the last successful pull, its
timestamp, and job count. This way a failure is visible through status information
instead of a silent crash or stale data with no signal anything's wrong.

For the demo I used RemoteOK's public JSON endpoint rather than LinkedIn or Indeed,
staying within the assignment's own scope guardrail rather than risking a real account
or ToS breach.

## 2. One trade-off made because of the time limit

I left out a browser-automation/proxy layer for sources that need JS rendering or have
stronger anti-bot protections — RemoteOK's public endpoint didn't need it, so adding one
just for the demo felt unjustified.

With a real week I'd add: a persistent database (PostgreSQL) instead of in-memory
results, schema/response-shape change detection, better failure logging and alerts, a
Playwright-based fallback for JS-heavy sources, and scheduling so past pulls can be
stored and compared over time.

## 3. Where I used AI tools, and what I verified myself

I used AI assistance while developing parts of the FastAPI service — the initial
structure, the retry/backoff logic, and environment/deployment setup. I didn't rely on
generated code without testing it: I ran the project locally and checked each piece
separately — the raw API request, then the retry wrapper, then the FastAPI endpoints,
then the live deployment — making changes myself whenever something didn't behave as
expected. The final implementation was tested locally before I pushed and deployed it.