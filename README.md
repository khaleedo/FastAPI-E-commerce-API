# FastAPI E-commerce API

[![CI](https://github.com/khaleedo/FastAPI-E-commerce-API/actions/workflows/ci.yml/badge.svg)](https://github.com/khaleedo/FastAPI-E-commerce-API/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]

A production-ready **FastAPI** backend for an e-commerce platform, built with **PostgreSQL**, **Docker**, and deployed on **Kubernetes** with **CI/CD via GitHub Actions**.

---

## ✨ Features
- User authentication with JWT  
- Role-based access control (admin, customer)  
- Product listings & order management  
- PostgreSQL database integration  
- Docker containerization & Kubernetes manifests  
- CI/CD with GitHub Actions and deployment to AWS EKS  

---

## Prerequisites
- Python 3.11+  
- Docker  
- kubectl configured for your cluster (EKS, minikube, kind, etc.)  
- GitHub account (for GHCR and Actions)  
- AWS CLI configured with credentials  
- Terraform CLI  

---

## 🚀 Quickstart — Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/khaleedo/FastAPI-E-commerce-API.git
cd <your-repo>
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment variables
Create a `.env` file in the project root (example):
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ecommerce_db
SECRET_KEY=your_super_secret_key_here
```

### 5. Initialize DB (Alembic) — if project includes migrations
```bash
# Example (adjust paths to your alembic setup)
alembic upgrade head
```

### 6. Run the FastAPI app
```bash
uvicorn main:app --reload
```
Open API docs: `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc`.

---

## 🐳 Run with Docker (local test)
Build the image:
```bash
docker build -t ecommerce-api:latest .
```

Run PostgreSQL (local Docker)
```bash
docker run --name fastapi-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ecommerce_db -p 5432:5432 -d postgres:15
```

Run the app container (link to local Postgres)
```bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/ecommerce_db" \
  -e SECRET_KEY="your_super_secret_key_here" \
  ecommerce-api:latest
```
> Note: On Linux, replace `host.docker.internal` with `localhost` or the proper host IP.

---

## ☸️ Deploy on Kubernetes (AWS EKS — minimal steps)

1. Create EKS Cluster with Terraform

Terraform files are in infra/:

main.tf → providers + VPC + EKS cluster

nodes.tf → managed node group

iam.tf → IAM roles and policies

variables.tf → input vars (region, cluster name, etc.)

outputs.tf → kubeconfig + cluster outputs

cd infra
terraform init
terraform plan
terraform apply -auto-approve

2. Connect kubectl to EKS
aws eks --region <your-region> update-kubeconfig --name <cluster-name>
kubectl get nodes

3. Deploy PostgreSQL
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml

4. Deploy FastAPI app
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml   


## ⚙️ CI/CD with GitHub Actions (overview)

This repo uses GitHub Actions to:

1. Run tests and linters on push / pull-request (branches: `main`, `develop`).  
2. Build Docker image and push to GitHub Container Registry (GHCR) on `main`.  
3. Deploy to Kubernetes (AWS EKS) from `main` using AWS credentials configured as GitHub Secrets.

### Important GitHub Secrets
Add these to your repository **Settings → Secrets**:
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` — for EKS update-kubeconfig + kubectl actions.  
- `AWS_REGION` — region of your EKS cluster.  
- `EKS_CLUSTER_NAME` — cluster name.  
- `CR_PAT` or use `GITHUB_TOKEN` for ghcr auth (if using GHCR).  
- Any DB credentials you don’t store in Kubernetes Secrets directly.

### Typical pipeline steps (high level)
- Checkout code  
- Set up Python, cache pip, install deps  
- Run `pytest` tests and `flake8` linting  
- Build Docker image and push to registry (tags: branch, sha)  
- Configure AWS credentials and update kubeconfig for EKS  
- `kubectl apply -f k8s/` and `kubectl rollout status` to validate

---

## ✅ Best practices & notes
- **Do not** hardcode secrets in YAML — use Kubernetes Secrets or a secrets manager (AWS Secrets Manager, HashiCorp Vault).  
- Use `imagePullPolicy: Always` in deployments for CI-published images on `latest` tag. Better: use immutable tags (sha) created by CI.  
- Add health endpoints (`/health`) so readiness/liveness probes work reliably.  
- Add logging and monitoring (Prometheus metrics or a hosted APM).  
- Add `pytest` unit tests and some integration tests to prove correctness.

---

## Troubleshooting
- `Connection refused` to Postgres: ensure Postgres pod/service is running and `DATABASE_URL` is correct.  
- Pod stuck in `CrashLoopBackOff`: check `kubectl logs <pod>` and `kubectl describe pod <pod>` for probe failures or startup exceptions.  
- Ingress not reachable: ensure ingress controller is installed and you used the correct external IP or DNS mapping.

---

## Contributing
1. Fork the repo  
2. Create a feature branch `git checkout -b feat/awesome`  
3. Commit and push, open a PR targeting `develop` (or `main`)  
4. Ensure CI passes

---

## License
MIT — feel free to reuse and adapt for demos or interviews.

---

## Contact
If you want this README tweaked (add badges, custom commands, or team-conventions), open an issue or DM me on GitHub.
