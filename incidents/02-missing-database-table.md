# Incident 02: Missing Database Table

## Summary
The ticket API returned HTTP 503 after the expected database table was renamed.

## Symptoms
- `GET /tickets` returned HTTP 503 Service Unavailable.
- The API returned a generic database error message.
- API logs recorded the failed request with status 503.

## Investigation
1. Confirmed the endpoint worked before the incident.
2. Renamed `support_tickets` to `support_tickets_backup`.
3. Retested the endpoint and observed HTTP 503.
4. Restored the original table name.
5. Retested and confirmed HTTP 200 with all three tickets.

## Root Cause
The application queried `support_tickets`, but that table name was temporarily unavailable because it had been renamed.

## Resolution
Renamed `support_tickets_backup` back to `support_tickets`.

## Verification
`GET /tickets` returned HTTP 200 and all three expected tickets.

## Lessons Learned
- Check schema and table names when database-backed endpoints fail.
- Confirm the actual database error before concluding the cause in a production incident.
- Verify recovery through the affected API endpoint.
