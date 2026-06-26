building it yourself file-by-file is how this actually sticks. Here's the order, with the *why* at each step and a way to verify it worked before moving on.

## 1. Project root + virtual environment

```bash
mkdir mlops-pipeline-demo && cd mlops-pipeline-demo
python -m venv venv
source venv/bin/activate        # Windows (PowerShell): venv\Scripts\Activate.ps1
```

## 2. `requirements.txt` — before any code

Dependencies first, so when you write imports in step 3 they actually resolve.

```
fastapi==0.138.1
uvicorn[standard]==0.49.0
pydantic==2.13.4
pytest==9.1.1
httpx==0.28.1
```

```bash
pip install -r requirements.txt
```

## 3. `app/model.py` — the "model" first, with zero dependencies on the API layer

```bash
mkdir app
touch app/__init__.py
```

`app/model.py`:
```python
def predict(value: float) -> float:
    """Dummy 'model': multiplies the input by 2."""
    return value * 2
```

This file knows nothing about HTTP, FastAPI, or anything else — that's deliberate. Sanity check it directly, no server needed:

```bash
python -c "from app.model import predict; print(predict(21))"
# 42.0
```

## 4. `app/main.py` — wrap the model in an API

```python
from fastapi import FastAPI
from pydantic import BaseModel

from app.model import predict

app = FastAPI(title="Hello World MLOps API")


class PredictRequest(BaseModel):
    value: float


class PredictResponse(BaseModel):
    result: float


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(payload: PredictRequest) -> PredictResponse:
    return PredictResponse(result=predict(payload.value))
```

`/health` exists purely for Cloud Run later — it pings that endpoint to know your container is alive. Run it and poke it by hand:

```bash
uvicorn app.main:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"value": 21}'
# {"result":42.0}
```

You just did manually what the test suite will do automatically — that's the next step, and why it comes after, not before.

## 5. `tests/test_main.py` — automate what you just did by hand

```bash
mkdir tests
touch tests/__init__.py
```

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_predict_doubles_value():
    response = client.post("/predict", json={"value": 21})
    assert response.json() == {"result": 42}
```

```bash
pytest -v
# 2 passed
```

This is the **CI foundation** — there's literally nothing to automate in step 8 if this file doesn't exist.

## 6. `.gitignore` — before `git init`, not after

```
__pycache__/
*.pyc
.pytest_cache/
venv/
.venv/
```

Order matters here: if you `git init` first and add files before this exists, you risk accidentally committing `venv/` (hundreds of MB of installed packages).

## 7. Push to GitHub — with no automation yet

```bash
git init
git add .
git commit -m "Hello world MLOps pipeline"
gh repo create mlops-pipeline-demo --public --source=. --push
```

Go look at the **Actions** tab on GitHub. It'll be empty. That's expected — GitHub doesn't run anything automatically until a workflow file tells it to.

## 8. `.github/workflows/ci-cd.yml` — CI only, deliberately incomplete

```bash
mkdir -p .github/workflows
```

Write **only** the test job for now — adding the deploy job before you've set up GCP just gives you a confusing red ❌ for the wrong reason:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -v
```

```bash
git add . && git commit -m "Add CI" && git push
```

Watch the Actions tab — you should see this job run and go green. **This is the actual CI milestone.** Try breaking a test on purpose and pushing again to see the red ❌; that feedback loop is the whole point of CI.

## 9. `Dockerfile` + `.dockerignore` — containerize, test locally

```
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
```

```
# .dockerignore
__pycache__/
.pytest_cache/
tests/
.git/
venv/
```

If you have Docker installed locally, verify it works **before** any CI/CD touches it:

```bash
docker build -t mlops-demo-api .
docker run -p 8080:8080 mlops-demo-api
curl http://localhost:8080/health
```

## 10. GCP setup (no files yet — just `gcloud` commands)

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

gcloud artifacts repositories create mlops-demo-repo \
  --repository-format=docker --location=us-central1

gcloud iam service-accounts create github-actions-deployer

PROJECT_ID=$(gcloud config get-value project)
SA_EMAIL=github-actions-deployer@${PROJECT_ID}.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/run.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/artifactregistry.writer"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts keys create key.json --iam-account=$SA_EMAIL
```

On GitHub: **Settings → Secrets and variables → Actions** → add `GCP_PROJECT_ID` and `GCP_SA_KEY` (paste the entire contents of `key.json`). Then delete `key.json` locally — never commit it.

## 11. Extend `ci-cd.yml` — add the deploy job now that secrets exist

Append this job to the same file from step 8:

```yaml
  build-and-deploy:
    name: Build, push, and deploy
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - uses: google-github-actions/setup-gcloud@v2
      - run: gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
      - run: docker build -t us-central1-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/mlops-demo-repo/mlops-demo-api:${{ github.sha }} .
      - run: docker push us-central1-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/mlops-demo-repo/mlops-demo-api:${{ github.sha }}
      - run: |
          gcloud run deploy mlops-demo-api \
            --image us-central1-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/mlops-demo-repo/mlops-demo-api:${{ github.sha }} \
            --project ${{ secrets.GCP_PROJECT_ID }} --region us-central1 \
            --platform managed --allow-unauthenticated
```

## 12. Push and watch the full loop

```bash
git add . && git commit -m "Add CD to Cloud Run" && git push
```

Watch Actions: `test` → `build-and-deploy`, in that order, the second only firing if the first goes green. When it finishes:

```bash
gcloud run services list
```

gives you the live URL.

## 13. Prove the loop works

Change `value * 2` to `value * 3` in `app/model.py`, commit, push. Time how long it takes from `git push` to the live URL returning the new result — that round-trip is everything you just built, working as one system.

---

Since you've already got the working zip from before, you can diff your from-scratch version against it at any step if something doesn't match and you're not sure why.