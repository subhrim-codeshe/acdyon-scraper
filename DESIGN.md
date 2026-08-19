# Design Document — Job Listing Ingestion Pipeline

**Live demo:** https://acdyon-scraper-vmeg.onrender.com/jobs (also see `/status`)
**Repo:** https://github.com/subhrim-codeshe/acdyon-scraper

## 1. Detection Surface

Platforms such as LinkedIn, Indeed, Naukri, and Wellfound can identify automated clients using several different signals:

* **Headless browser fingerprints** — things like missing or inconsistent `navigator` properties, unusual browser plugins or fonts, or WebDriver flags that are commonly left enabled by Selenium or Puppeteer.
* **Request timing** — requests that happen at perfectly regular intervals or pages being accessed much faster than a normal person could browse them.
* **Headers and connection details** — missing headers such as `Accept-Language`, mismatches between the `User-Agent` and other connection fingerprints, or missing `Referer` information that would normally be present in a browser session.
* **Behavior patterns** — automated clients may not show normal actions such as scrolling or mouse movement, or may repeat exactly the same session behavior across multiple requests.
* **Request volume** — a single IP or identity making significantly more requests than would normally be expected from a human user.

For my current demo, I am using a public and unauthenticated API, so I only need a basic descriptive `User-Agent` header. The source does not require browser-level fingerprint handling.

If this were being used with a more protected platform such as LinkedIn, there would be additional challenges around these detection signals.

## 2. Ingestion Strategy

For the demo, I use a single `httpx` client with a custom `User-Agent`. The request is also wrapped in a retry mechanism with exponential backoff. It makes up to 3 attempts, waiting approximately 1 second, 2 seconds, and 4 seconds between retries.

The main purpose of this is to handle temporary failures without stopping the entire ingestion process.

For a more complex real-world source, the same basic structure could be extended with:

* **Identity rotation** — using a pool of residential or mobile proxies instead of relying on a single IP for all requests.
* **Request pacing** — adding some variation to the time between requests instead of sending them at fixed intervals.
* **Session management** — maintaining cookies or local storage for individual sessions so that requests are not completely stateless.
* **Handling blocks during a run** — if an identity starts receiving repeated CAPTCHA challenges or 403 responses, it could be temporarily taken out of rotation and placed on cooldown instead of immediately retrying the same request.

These are design considerations for a more advanced implementation and were not required for the current demo.

## 3. Resilience

The `/status` endpoint is the main visible part of the resilience handling in the current implementation. It shows the timestamp of the last pull, the number of jobs retrieved, and whether the last pull succeeded or failed.

This makes it easier to notice when the source stops working instead of silently continuing with old or missing data.

For a production version, I would add:

* **Markup or schema-change detection** — compare the response structure with a previously known structure and raise an alert if the source changes unexpectedly.
* **Empty-response handling** — this is already implemented. If the source returns an empty result, the system retries instead of immediately assuming that there are no jobs.
* **Circuit breaker** — if a source continues failing, temporarily stop making requests to it and wait for a cooldown period before trying again.
* **Dead-letter logging** — store failed pulls with information such as the timestamp, source, and error so that they can be investigated later.

## 4. Where I'd Stop

I did not run this pipeline directly against LinkedIn, Indeed, Naukri, or Wellfound. The live demo uses a source with a genuinely public and unauthenticated API, which is within the scope of the assignment.

My approach is that I would not scrape behind an authentication wall using a real account, bypass CAPTCHAs that are specifically intended to prevent automation, or ignore a platform's `robots.txt` or explicit anti-scraping rules.

The technical points above explain how a more advanced ingestion system could deal with detection and blocking, but I did not build or test those mechanisms against a real protected platform. That would go beyond the scope of the demo and the guardrails given in the assignment.
