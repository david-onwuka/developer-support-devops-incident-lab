# Incident Report: PostgreSQL Availability Failure

## Summary
A controlled incident simulation tested API behavior when the PostgreSQL deployment was unavailable.

## Impact
The API's `/tickets` endpoint depends on PostgreSQL. During the simulation, ticket retrieval was expected to fail while the database had zero replicas.

## Detection and Diagnosis
Checked Kubernetes pod status with `kubectl get pods` and identified that the PostgreSQL deployment had been scaled to zero replicas.

## Recovery
Restored the PostgreSQL deployment to one replica:

`kubectl scale deployment/support-postgres --replicas=1`

Confirmed recovery with:

`kubectl rollout status deployment/support-postgres`

Both the API and PostgreSQL pods returned to `Running`.

## Verification
The API's `/tickets` endpoint returned `HTTP/1.1 200 OK` and all three seeded support tickets after recovery.

## Root Cause
Intentional scaling of the PostgreSQL deployment to zero replicas for this controlled test.

## Preventive Measures
- Monitor database pod availability and API database errors.
- Keep readiness checks and useful application logs.
- Document recovery steps and verify dependent endpoints after restoration.

## Notes
This was a controlled portfolio exercise, not a production incident. The port-forward also stopped during the exercise and had to be restarted before final API verification.
