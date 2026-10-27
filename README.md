# Developer Support & DevOps Incident Lab

[![Tests](https://github.com/david-onwuka/developer-support-devops-incident-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/david-onwuka/developer-support-devops-incident-lab/actions/workflows/tests.yml)
[![Publish image](https://github.com/david-onwuka/developer-support-devops-incident-lab/actions/workflows/publish-image.yml/badge.svg)](https://github.com/david-onwuka/developer-support-devops-incident-lab/actions/workflows/publish-image.yml)

A hands-on lab for investigating application issues, troubleshooting database connectivity, deploying containerized services, and documenting incident recovery.

A FastAPI application backed by PostgreSQL, run with Docker Compose, tested with pytest, built and published by GitHub Actions to GitHub Container Registry (GHCR), and deployed to Kubernetes.

**Container image:** `ghcr.io/david-onwuka/developer-support-devops-incident-lab:latest`

## Proof at a glance

- API deployed to Kubernetes. `/health` returned HTTP 200 and `/tickets` returned HTTP 200 with three tickets.
- PostgreSQL storage backed by a 1 GiB PersistentVolumeClaim, verified as `Bound`.
- Database connection string supplied through a Kubernetes Secret, not hardcoded in the manifest.
- Two GitHub Actions workflows, one for tests and one for publishing the image to GHCR.
- A documented PostgreSQL outage and recovery exercise, with the API verified after recovery.

![Kubernetes API health and tickets](docs/screenshots/kubernetes-api-health-and-tickets.png)

> **Note:** The Kubernetes deployment ran in a Killercoda lab environment, which has since expired. The manifests in `k8s/` and the screenshots below are the evidence of that deployment.

## Why I built this

I wanted to bring application support and DevOps operations together in one project. Instead of only writing an API, I worked through running a service, checking its dependencies, testing its behaviour, deploying it to Kubernetes, and documenting how to investigate and recover from infrastructure problems.

## Technology stack

- **Python, FastAPI:** REST API
- **PostgreSQL:** relational storage for support tickets
- **Docker, Docker Compose:** containerization and local environment
- **pytest:** automated tests
- **GitHub Actions:** test and image publishing workflows
- **GHCR:** image storage and distribution
- **Kubernetes:** deployment, service discovery, persistent storage

## Architecture

```text
Client
  |
  v
FastAPI Application
  |
  | SQL connection
  v
PostgreSQL Database
  |
  v
Support Ticket Records
```

In Kubernetes, the API and PostgreSQL run as separate Deployments. Services provide network access, and a PersistentVolumeClaim provides PostgreSQL storage.

```text
GitHub Repository
       |
       v
GitHub Actions
       |
       +----> Run automated tests
       |
       +----> Build and publish image
                       |
                       v
                     GHCR
                       |
                       v
                Kubernetes Cluster
                  /           \
                 v             v
           FastAPI API     PostgreSQL
                                |
                                v
                        PersistentVolume
```

## Getting started

### Prerequisites

- Git
- Python
- Docker and Docker Compose
- For the Kubernetes deployment: a cluster and `kubectl`

### Run with Docker Compose

```bash
git clone https://github.com/david-onwuka/developer-support-devops-incident-lab.git
cd developer-support-devops-incident-lab
docker compose up --build -d
docker compose ps
```

View logs when investigating a problem:

```bash
docker compose logs api
docker compose logs postgres
```

Stop the environment:

```bash
docker compose down
```

### Run the tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Returns service status information. |
| GET | `/health` | Checks application health. |
| GET | `/tickets` | Retrieves support tickets from the database. |

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/tickets
```

In the Kubernetes deployment, `/health` returned HTTP 200 with `{"status": "healthy"}`. `/tickets` returned HTTP 200 with three sample tickets: an API HTTP 500 error, a database connection timeout, and a ticket endpoint returning no data. These are the kinds of issues a support engineer investigates.

## CI/CD

Two workflows live in `.github/workflows/`:

- `tests.yml` runs the pytest suite.
- `publish-image.yml` builds the application image and publishes it to GHCR.

Keeping them separate means validating a change and distributing an image are independent steps.

## Kubernetes deployment

Manifests and deployment instructions are in [`k8s/`](k8s/README.md). The deployment includes:

- A PostgreSQL Deployment and a FastAPI Deployment.
- A PostgreSQL Service (`support-postgres`) for in-cluster connectivity.
- An API Service exposed through NodePort `31703` in the lab configuration.
- A PersistentVolumeClaim (`support-postgres-pvc`, 1 GiB) for PostgreSQL storage.
- A ConfigMap for database initialization.
- A Secret holding the database connection configuration. The credentials are demonstration credentials, not production ones.

After applying the manifests, I checked resource status, confirmed both pods were running, and verified the endpoints. To test from a local terminal:

```bash
kubectl port-forward service/support-api 8000:8000
curl -i http://localhost:8000/health
curl -i http://localhost:8000/tickets
```

Keep port forwarding running while you make the requests. Stop it with `Ctrl+C`.

## PostgreSQL outage and recovery exercise

I simulated a database outage by scaling the PostgreSQL Deployment to zero replicas, then restored it:

```bash
kubectl scale deployment/support-postgres --replicas=0
kubectl scale deployment/support-postgres --replicas=1
```

After restoring, I confirmed the workloads were running, restarted port forwarding, and verified `/tickets` returned HTTP 200 with all three sample tickets.

Full write-up: [PostgreSQL Outage and Recovery Report](incidents/postgres-outage-recovery.md)

## Evidence

**API health and ticket retrieval.** Health and ticket endpoint responses from the Kubernetes deployment.

![Kubernetes API health and tickets](docs/screenshots/kubernetes-api-health-and-tickets.png)

**Kubernetes resources.** Application and database workloads, Services, and the bound PersistentVolumeClaim.

![Kubernetes resource status](docs/screenshots/kubernetes-resources-status.png)

**Automated tests.** A successful GitHub Actions test run.

![GitHub Actions tests success](docs/screenshots/github-actions-tests-success.png)

**Image publishing.** A successful GitHub Actions run publishing the image to GHCR.

![GitHub Actions image publishing success](docs/screenshots/github-actions-image-publish-success.png)

## Repository structure

```text
developer-support-devops-incident-lab/
├── .github/workflows/   # tests.yml, publish-image.yml
├── app/                 # FastAPI application
├── docs/screenshots/    # Deployment and CI/CD evidence
├── incidents/           # Incident reports
├── k8s/                 # Kubernetes manifests and deployment guide
├── tests/               # Automated tests
├── Dockerfile
├── docker-compose.yml
├── init.sql             # Database initialization
├── requirements.txt
└── README.md
```

## Future improvements

- Add readiness and liveness probes to the Kubernetes Deployments.
- Add resource requests and limits.
- Tag images with the commit SHA instead of relying on `latest`.
- Add integration tests for database-unavailable and missing-table scenarios.
- Add a database backup and restore exercise.
- Add structured logs and metrics.
- Add a Secret creation example that avoids committing real credentials.

## Author

**Eme David Onwuka**

Technical Support | Developer Support | DevOps | Infrastructure & Databases

- GitHub: [david-onwuka](https://github.com/david-onwuka)
