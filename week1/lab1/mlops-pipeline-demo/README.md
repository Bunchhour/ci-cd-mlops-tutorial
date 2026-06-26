# Hello World MLOps Pipeline

A minimal FastAPI app serving a dummy "model" (multiplies a number by 2),
tested with pytest, containerized with Docker, and deployed to Cloud Run
via GitHub Actions. Built to practice CI/CD fundamentals end-to-end.

Practice this in stages — don't jump straight to the full pipeline.
Each stage below should *visibly work* before you move to the next one.

---

## Stage 0 — Run it locally (no CI/CD yet)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
# Visit http://127.0.0.1:8000/docs to try /predict interactively

# In another terminal, run the tests
pytest -v
```

You should see 4 passing tests. This is your "it works on my machine" baseline —
everything after this is about making it work *without* your machine.

## Stage 1 — Push to GitHub, get CI working (no GCP yet)

```bash
git init
git add .
git commit -m "Hello world MLOps pipeline"
gh repo create mlops-pipeline-demo --public --source=. --push
# (or create the repo on github.com and `git remote add origin ...` + push manually)
```

Go to the **Actions** tab on GitHub. You'll see the `test` job run automatically.
Comment out the `build-and-deploy` job in `.github/workflows/ci-cd.yml` for now
if you don't want it failing on missing GCP secrets — or just let it fail and
fix it in Stage 2. Either is fine; failure here is informative, not scary.

Try breaking a test on purpose (e.g. change `result=42` expectation) and push —
watch the red ❌. That feedback loop *is* CI.

## Stage 2 — Wire up GCP for CD

1. **Create a GCP project** (or use an existing one) and note the Project ID.
2. **Enable APIs:**
   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com
   ```
3. **Create an Artifact Registry repo** (name must match `REPOSITORY` in the workflow):
   ```bash
   gcloud artifacts repositories create mlops-demo-repo \
     --repository-format=docker \
     --location=us-central1
   ```
4. **Create a service account** for GitHub Actions to authenticate as:
   ```bash
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
5. **Add GitHub repo secrets** (Settings → Secrets and variables → Actions):
   - `GCP_PROJECT_ID` → your project ID
   - `GCP_SA_KEY` → the *entire contents* of `key.json`

   Then delete `key.json` locally — don't commit it.

6. Push any small change to `main`. Watch the Actions tab run `test` →
   `build-and-deploy`. When it finishes, `gcloud run services list` will show
   your live URL.

## Stage 3 — Close the loop

Change `app/model.py` so it multiplies by 3 instead of 2, push, and time how
long it takes from `git push` to the live endpoint reflecting the change.
That round-trip is the entire point of the exercise.

---

## Where to go from here

- Swap `app/model.py` for a real model (load a pickled sklearn model,
  call a Groq/Gemini API, etc.) — nothing else needs to change.
- Add a staging environment: deploy PRs to a separate Cloud Run service
  before merging to main.
- Add model-specific tests: schema validation on inputs, latency budgets,
  a fixed-input/fixed-output regression test so a redeploy can't silently
  change model behavior.
