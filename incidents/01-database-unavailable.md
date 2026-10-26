# Incident 01: Database Unavailable

## Summary
The ticket API returned HTTP 503 when PostgreSQL became unavailable.

## Symptoms
- `GET /tickets` returned HTTP 503 Service Unavailable.
- Response: `{"detail":"Unable to retrieve support tickets"}`
- Docker showed the database container as stopped.
- API logs recorded the failed request with status 503.

## Investigation
1. Checked the API before the incident; it returned HTTP 200.
2. Stopped PostgreSQL to simulate a database outage.
3. Repeated the request and observed HTTP 503.
4. Checked API logs and container status.
5. Restarted PostgreSQL and confirmed it became healthy.

## Root Cause
The PostgreSQL container was deliberately stopped during incident simulation, preventing the API from connecting to its database.

## Resolution
Restarted PostgreSQL using `docker compose start db`.

## Verification
After PostgreSQL became healthy, `GET /tickets` returned HTTP 200 and all three expected tickets.

## Lessons Learned
- Check service health and container status before changing application code.
- Verify the impact using the affected endpoint.
- Confirm recovery with a successful request.
- Improve application-side logging to capture database exceptions without exposing internal details to API clients.
