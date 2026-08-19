# DECISIONS.md

## 1. Why I chose this ingestion approach

At first, I considered making a simple scraper that would fetch the source once and fail if something went wrong. I decided against that because a real ingestion pipeline needs to handle temporary problems like an empty response, rate limiting, or a change in the source format.

Instead, I added a small fetch layer with retries and exponential backoff. It tries up to 3 times, with the wait time increasing after each failed attempt. I also added a `/status` endpoint that shows the last successful pull, when it happened, and how many jobs were returned.

This way, if the source stops working, the service doesn't just crash or continue showing old data without any indication. The failure is visible through the status information.

For the demo, I used RemoteOK's public JSON endpoint instead of LinkedIn or Indeed. This keeps the implementation within the scope of the assignment and avoids dealing with protected accounts or potentially violating a site's terms of service.

If I were building this for a production system with sources that have stronger restrictions, I would look at things like proper rate limiting, authenticated APIs where available, and source-specific integrations rather than trying to bypass anti-bot protections.

## 2. One trade-off I made because of the time limit

The main thing I left out was a more advanced handling layer for sources that use JavaScript rendering or have stricter access controls.

For this demo, a normal HTTP client was enough because RemoteOK provides a public endpoint. I didn't think it made sense to add a browser automation or proxy system just for the demo when the selected source didn't require it.

If I had another week to work on the project, I would improve it by adding:

* A persistent database such as PostgreSQL instead of keeping results only in memory.
* Schema or response-shape checks to detect when the source format changes.
* Better logging and alerts when repeated fetches fail.
* A Playwright-based fallback for sources that genuinely require browser rendering.
* More robust scheduling so previous pulls can be stored and compared over time.

## 3. Where I used AI tools and what I verified myself

I used AI assistance while developing parts of the FastAPI service, especially for the initial service structure, retry/backoff logic, and environment setup.

I did not rely on the generated code without testing it. I ran the project locally and checked each part separately: first the raw API request, then the retry logic, then the FastAPI endpoints, and finally the deployed version.

I also made changes while testing whenever something didn't behave as expected. The final implementation was tested by me locally before it was pushed and deployed.

The main thing I took from the AI assistance was help with getting the initial implementation and structure in place. I still verified that the code actually worked with the selected data source and that the endpoints behaved as expected.
