# Incident 03: Database Error Logging

## Objective
Improve diagnosis of database failures without exposing internal details to API clients.

## Test
Renamed the expected table, support_tickets, to support_tickets_backup.

## Observed Result
- API returned HTTP 503.
- Client received a generic error message.
- Application logs captured the database exception and traceback.
- PostgreSQL reported: UndefinedTable — relation "support_tickets" does not exist.

## Resolution
Restored the original table name and verified the API recovered.

## Improvement
The application now uses Python logging with logger.exception() to capture diagnostic details while returning a generic response to clients.
