# Kubernetes Deployment

## Prerequisites
- A Kubernetes cluster with kubectl configured.
- The repository cloned locally.
- The API image available at GHCR.

## Deploy

Run these commands from the repository root.

1. Create the database Secret:

   kubectl create secret generic support-db-secret \
     --from-literal=POSTGRES_USER=support_user \
     --from-literal=POSTGRES_PASSWORD=change_me_k8s \
     --from-literal=POSTGRES_DB=support_lab \
     --from-literal=DATABASE_URL=postgresql://support_user:change_me_k8s@support-postgres:5432/support_lab

   Replace the example password with a suitable value for your environment.
   Keep real credentials out of Git.

2. Apply the database initialization ConfigMap:

   kubectl apply -f k8s/db-configmap.yaml

3. Create storage and deploy PostgreSQL:

   kubectl apply -f k8s/postgres-pvc.yaml
   kubectl apply -f k8s/postgres-deployment.yaml

4. Deploy the API:

   kubectl apply -f k8s/api-deployment.yaml

5. Check deployment status:

   kubectl get pods,services,pvc
   kubectl rollout status deployment/support-postgres
   kubectl rollout status deployment/support-api

## Test the API

Forward the API service port:

   kubectl port-forward service/support-api 8000:8000

In another terminal:

   curl http://127.0.0.1:8000/health
   curl -i http://127.0.0.1:8000/tickets

Expected: the health endpoint reports healthy, and the tickets endpoint returns the seeded support tickets.

Note: the PostgreSQL initialization script runs only when the database data directory is first initialized. Existing persistent data is not reseeded automatically.
