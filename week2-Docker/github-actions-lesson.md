# GitHub Actions — Complete Lesson Guide

> **Purpose:** A structured, hands-on lesson guide for mastering GitHub Actions CI/CD.
> **Audience:** Students and developers building CI/CD and MLOps pipelines.
> **Format:** Each lesson has learning objectives, concept explanation, YAML examples, and practice exercises.

---

## Table of Contents

| Lesson | Topic |
|--------|-------|
| Lesson 1 | What is GitHub Actions? Core Concepts |
| Lesson 2 | Anatomy of a Workflow YAML File |
| Lesson 3 | Triggers (on:) — When Workflows Run |
| Lesson 4 | Jobs & Runners |
| Lesson 5 | Steps — uses vs run |
| Lesson 6 | Environment Variables & Secrets |
| Lesson 7 | Strategy Matrix — Parallel Testing |
| Lesson 8 | Artifacts & Dependency Caching |
| Lesson 9 | Building a Full CI Pipeline |
| Lesson 10 | Building a CD Pipeline — Auto Deployment |
| Lesson 11 | Reusable Workflows & Composite Actions |
| Lesson 12 | Real-World MLOps CI/CD Workflow |
| Lesson 13 | Debugging & Common Pitfalls |
| Quick Reference | Cheat Sheet |

---

## Lesson 1: What is GitHub Actions? Core Concepts

### Learning Objectives
- Understand what GitHub Actions is and how it fits in the developer workflow
- Know the terminology: Workflow, Job, Step, Runner, Action

### Concept

**GitHub Actions** is a CI/CD automation platform built directly into GitHub. It watches your repository for events (a push, a pull request, a schedule) and automatically executes scripts in response — on fresh, cloud-hosted machines.

#### The Three Layers — Git vs GitHub vs GitHub Actions

| Layer | What It Is | Analogy |
|-------|-----------|---------|
| **Git** | Local version control tool. Tracks file history, branches, merges. | Save/undo system for your codebase |
| **GitHub** | Cloud hosting for Git repos. Where your team collaborates. | Shared cloud drive for your repo |
| **GitHub Actions** | Automation engine built into GitHub. Reacts to repo events. | A robot that watches your repo and does work when things happen |

> You can use Git without GitHub. You can use GitHub without Actions. But Actions requires GitHub.

#### Core Terminology

| Term | Definition |
|------|-----------|
| **Workflow** | A YAML file inside `.github/workflows/`. Defines triggers and jobs. |
| **Trigger (on:)** | The event that starts the workflow (push, pull_request, schedule, etc.) |
| **Job** | A unit of work that runs in its own fresh container/VM |
| **Runner** | The machine that executes the job (GitHub-hosted or self-hosted) |
| **Step** | A single task inside a job — either a shell command or a reusable Action |
| **Action** | A packaged, reusable step shared via the GitHub Marketplace |
| **Artifact** | A file produced by a workflow that is saved and can be downloaded or passed between jobs |

#### How It All Fits Together

```
Repository Event (push to main)
         |
         v
    Workflow triggered   (.github/workflows/ci.yml)
         |
         v
     Job: build-and-test
         |  runs-on: ubuntu-latest  (fresh virtual machine spun up)
         |
         v
     Step 1: actions/checkout@v4   (clone the repo)
     Step 2: actions/setup-python@v5
     Step 3: pip install -r requirements.txt
     Step 4: pytest
         |
         v
    Job complete -> pass or fail reported to GitHub UI
```

### Practice Exercise
1. Go to any of your GitHub repositories
2. Click the **Actions** tab
3. Browse the starter workflow templates GitHub suggests
4. Identify: what is the trigger? how many jobs? how many steps per job?


---

## Lesson 2: Anatomy of a Workflow YAML File

### Learning Objectives
- Read and understand every section of a workflow file
- Know what each top-level key does

### Concept

Every workflow file is a YAML file placed in `.github/workflows/` in your repository. The filename can be anything (e.g., `ci.yml`, `deploy.yml`). GitHub automatically detects all files in that folder.

### Annotated Full Example

```yaml
# The display name shown in the GitHub Actions UI
name: Python CI Pipeline

# TRIGGER: which events cause this workflow to run
on:
  push:
    branches: ["main", "develop"]   # run when pushing to these branches
  pull_request:
    branches: ["main"]              # run when a PR targets main
  workflow_dispatch:                # allow manual trigger from the Actions tab

# JOBS: define one or more parallel/sequential units of work
jobs:

  # JOB ID (used to reference this job from other jobs)
  test:

    # RUNNER: which OS/machine this job runs on
    runs-on: ubuntu-latest

    # STEPS: ordered list of tasks inside this job
    steps:

      # STEP 1: Clone the repository into the runner
      - name: Checkout code
        uses: actions/checkout@v4     # uses a pre-built Action

      # STEP 2: Set up a specific Python version
      - name: Set up Python
        uses: actions/setup-python@v5
        with:                         # parameters passed to the Action
          python-version: "3.11"

      # STEP 3: Install dependencies using a shell command
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # STEP 4: Run tests
      - name: Run pytest
        run: pytest --verbose
```

### Top-Level Keys Reference

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | No | Label shown in the GitHub UI |
| `on` | Yes | Event triggers that start this workflow |
| `jobs` | Yes | Defines all jobs to run |
| `env` | No | Global environment variables available to all jobs |
| `permissions` | No | GitHub token permission scopes |
| `defaults` | No | Default `run` settings (working directory, shell) |

### Inside a Job

| Key | Required | Purpose |
|-----|----------|---------|
| `runs-on` | Yes | The runner OS (ubuntu-latest, windows-latest, macos-latest) |
| `steps` | Yes | Ordered list of steps |
| `needs` | No | Wait for another job to finish first |
| `if` | No | Conditional: only run if this expression is true |
| `env` | No | Environment variables scoped to this job |
| `outputs` | No | Values this job exposes to downstream jobs |
| `strategy` | No | Matrix for running the job multiple times with different configs |

### Inside a Step

| Key | When Used | Purpose |
|-----|-----------|---------|
| `name` | Optional | Label shown in the UI for this step |
| `uses` | Use an Action | Run a pre-built action (e.g., `actions/checkout@v4`) |
| `run` | Run a command | Execute a shell command or multiline script |
| `with` | With `uses` | Parameters/inputs to pass to the Action |
| `env` | Optional | Environment variables scoped to this step only |
| `if` | Optional | Conditional: skip this step based on an expression |
| `id` | Optional | Reference this step's outputs later |
| `continue-on-error` | Optional | Allow workflow to continue even if this step fails |

> IMPORTANT: A step uses EITHER `uses` OR `run` — never both.

### Practice Exercise
Read this workflow snippet and answer the questions below:

```yaml
name: Deploy App
on:
  push:
    branches: ["main"]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

1. How many jobs are there?
2. What triggers this workflow?
3. Will `deploy` run if `build` fails? Why?
4. What does `needs: build` do?
5. Why does the `deploy` job also need `actions/checkout`?


---

## Lesson 3: Triggers (on:) — When Workflows Run

### Learning Objectives
- Know all the common trigger types
- Configure branch filters, path filters, and scheduled triggers

### Concept

The `on:` key defines WHEN a workflow starts. GitHub supports many event types.

### Common Trigger Types

#### Push & Pull Request Triggers
```yaml
on:
  push:
    branches:
      - main
      - "release/**"      # wildcard: any branch starting with release/
    paths:
      - "src/**"           # only trigger if files in src/ changed
      - "requirements.txt"
    paths-ignore:
      - "docs/**"          # skip if only docs changed
      - "**.md"            # skip if only markdown files changed

  pull_request:
    branches:
      - main
    types:
      - opened             # PR was opened
      - synchronize        # new commit pushed to PR branch
      - reopened           # PR was reopened
```

#### Scheduled Trigger (cron)
```yaml
on:
  schedule:
    - cron: "0 6 * * 1-5"    # Run at 6:00 AM UTC, Monday-Friday
    - cron: "0 0 * * 0"      # Also run at midnight every Sunday
```

Cron format: `minute  hour  day-of-month  month  day-of-week`

| Field | Values |
|-------|--------|
| minute | 0-59 |
| hour | 0-23 |
| day-of-month | 1-31 |
| month | 1-12 |
| day-of-week | 0-6 (0=Sunday) |

Common patterns:
```
0 * * * *      = every hour
0 0 * * *      = every day at midnight
*/15 * * * *   = every 15 minutes
0 9 * * 1      = every Monday at 9:00 AM
```

#### Manual Trigger (workflow_dispatch)
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Which environment to deploy to"
        required: true
        default: "staging"
        type: choice
        options:
          - staging
          - production
      run_tests:
        description: "Run tests before deploying?"
        required: false
        default: true
        type: boolean
```

This adds a "Run workflow" button in the GitHub Actions UI with a form for inputs.

#### Trigger on Another Workflow Finishing
```yaml
on:
  workflow_run:
    workflows: ["Python CI"]   # name of the other workflow
    types:
      - completed
```

#### Tag Push (useful for release automation)
```yaml
on:
  push:
    tags:
      - "v*"          # triggers on any tag like v1.0, v2.3.1
```

### Multiple Triggers Together
```yaml
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  schedule:
    - cron: "0 0 * * 0"
  workflow_dispatch:
```

All four triggers are active simultaneously. Any one of them can start the workflow.

### Practice Exercise

Write the `on:` block for these requirements:
1. Run on push to `main` or `develop` branches
2. Run on PRs targeting `main`
3. Run every day at midnight UTC automatically
4. Allow manual trigger with an input called `skip_tests` (boolean, default: false)


---

## Lesson 4: Jobs & Runners

### Learning Objectives
- Understand what a runner is and the types available
- Configure multiple jobs with dependencies between them

### Concept

A **Job** is an independent unit of work. Each job runs in its own fresh virtual machine (runner). Jobs run in **parallel by default** unless you explicitly set dependencies.

### GitHub-Hosted Runners

| Runner Label | OS | Notes |
|-------------|-----|-------|
| `ubuntu-latest` | Ubuntu Linux | Fastest, most common, cheapest |
| `ubuntu-22.04` | Ubuntu 22.04 LTS | Pin to a specific version |
| `ubuntu-20.04` | Ubuntu 20.04 LTS | Older, for legacy compatibility |
| `windows-latest` | Windows Server | Use for .NET, PowerShell, Windows-only tests |
| `macos-latest` | macOS | Use for iOS/macOS builds |
| `macos-13` | macOS 13 | Pin to a specific macOS version |

> Use `ubuntu-latest` by default — it is fastest and the most tools come pre-installed.

### Parallel Jobs (Default Behavior)

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: flake8 src/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bandit -r src/
```

All three jobs start simultaneously. The overall workflow passes only when ALL jobs pass.

### Sequential Jobs with `needs:`

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest

  build:
    runs-on: ubuntu-latest
    needs: test             # only runs AFTER test passes
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t my-app:latest .

  deploy:
    runs-on: ubuntu-latest
    needs: [test, build]    # waits for BOTH test AND build to pass
    steps:
      - run: ./deploy.sh
```

```
Workflow execution order:
  test ─────────────────────────► build ─────► deploy
  security-scan (parallel with test, no dependency)
```

### Passing Data Between Jobs with `outputs`

Jobs run in isolated environments. To share data, use job outputs:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.tag.outputs.tag }}   # expose output to other jobs
    steps:
      - name: Generate image tag
        id: tag
        run: echo "tag=v$(date +%Y%m%d%H%M%S)" >> $GITHUB_OUTPUT

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy image
        run: |
          echo "Deploying image tag: ${{ needs.build.outputs.image-tag }}"
          ./deploy.sh ${{ needs.build.outputs.image-tag }}
```

### Conditional Jobs

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'    # only deploy on main branch
    steps:
      - run: echo "Deploying to production..."
```

### Practice Exercise

Design a workflow with these jobs:
1. `lint` — checks code style (parallel)
2. `unit-test` — runs unit tests (parallel)
3. `integration-test` — runs integration tests, but only AFTER unit-test passes
4. `deploy-staging` — deploys, but only after ALL of lint, unit-test, integration-test pass
5. `deploy-prod` — deploys to production, after staging, only if branch is `main`

Draw the dependency graph, then write the `jobs:` section.


---

## Lesson 5: Steps — uses vs run

### Learning Objectives
- Know when to use `uses` (pre-built Action) vs `run` (shell command)
- Find and use Actions from the GitHub Marketplace
- Understand the most commonly used Actions

### Concept

Every step is one of two types:

| Type | Key | What It Does |
|------|-----|-------------|
| **Action** | `uses` | Runs a pre-packaged, reusable automation built by the community or GitHub |
| **Shell command** | `run` | Executes a raw terminal command directly in the runner |

### Using Pre-Built Actions (`uses`)

Actions are referenced as `owner/repo@version`:

```yaml
steps:
  # GitHub official actions
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
  - uses: actions/setup-node@v4
  - uses: actions/upload-artifact@v4
  - uses: actions/download-artifact@v4
  - uses: actions/cache@v4

  # Third-party actions
  - uses: docker/login-action@v3
  - uses: docker/build-push-action@v6
  - uses: aws-actions/amazon-ecr-login@v2
```

Always pin to a version tag (`@v4`, `@v3`) — never use `@main` or `@latest` in production. This prevents surprise breakage when action maintainers release updates.

### Passing Inputs to Actions (`with`)

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    cache: "pip"              # optional: cache pip packages automatically

- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

### Running Shell Commands (`run`)

```yaml
steps:
  # Single command
  - name: Run tests
    run: pytest

  # Multi-line script (use | for block literal)
  - name: Build and tag image
    run: |
      docker build -t my-app:${{ github.sha }} .
      docker tag my-app:${{ github.sha }} my-app:latest
      echo "Build complete"

  # Change working directory
  - name: Run backend tests
    working-directory: ./backend
    run: pytest tests/

  # Use a specific shell
  - name: PowerShell example
    shell: powershell
    run: Write-Host "Hello from PowerShell"
```

### Capturing Output from a Step

```yaml
steps:
  - name: Get current date
    id: date                    # give the step an id
    run: echo "date=$(date +%Y-%m-%d)" >> $GITHUB_OUTPUT

  - name: Use the date
    run: echo "Today is ${{ steps.date.outputs.date }}"
```

### Most Commonly Used Actions

#### actions/checkout@v4
```yaml
# Required in almost every job — clones your repo into the runner
- uses: actions/checkout@v4

# Options
- uses: actions/checkout@v4
  with:
    ref: develop              # checkout a specific branch
    fetch-depth: 0            # full git history (needed for git log, tags, etc.)
    submodules: true          # also checkout git submodules
```

#### actions/setup-python@v5
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    python-version-file: ".python-version"  # alternative: read version from file
    cache: "pip"              # auto-cache pip downloads
```

#### actions/setup-node@v4
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm"
```

#### actions/upload-artifact@v4 / download-artifact@v4
```yaml
# Upload a build artifact (e.g., test report, built binary)
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: reports/
    retention-days: 30

# Download it in another job
- uses: actions/download-artifact@v4
  with:
    name: test-results
    path: ./reports
```

### Practice Exercise

Complete the blank steps in this workflow:

```yaml
name: Node.js CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Step 1: Clone the repository
      - ___

      # Step 2: Set up Node.js version 20 with npm caching
      - ___
        with:
          node-version: "20"
          cache: "npm"

      # Step 3: Install npm packages
      - name: Install dependencies
        run: ___

      # Step 4: Run tests
      - name: Test
        run: ___

      # Step 5: Upload test coverage report (in coverage/ folder)
      - ___
        with:
          name: coverage-report
          path: coverage/
```


---

## Lesson 6: Environment Variables & Secrets

### Learning Objectives
- Set environment variables at different scopes (workflow, job, step)
- Store sensitive values as GitHub Secrets
- Use built-in GitHub context variables

### Concept

Never hardcode credentials, API keys, or passwords in your workflow files. GitHub provides a **Secrets** system for this. Environment variables let you pass configuration to your scripts.

### Setting Environment Variables

#### Workflow-level (available to all jobs and steps)
```yaml
env:
  APP_ENV: production
  LOG_LEVEL: info
  PYTHON_VERSION: "3.11"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running in $APP_ENV mode"
```

#### Job-level (available to all steps in this job only)
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: postgres://localhost:5432/testdb
    steps:
      - run: pytest --db-url $DATABASE_URL
```

#### Step-level (available to this step only)
```yaml
steps:
  - name: Build with specific config
    env:
      NODE_ENV: test
      API_BASE_URL: http://localhost:3000
    run: npm run build
```

### GitHub Secrets

Secrets are encrypted values stored in your repository or organization settings. They are NEVER visible in logs.

#### How to Add a Secret
1. Go to your GitHub repo -> Settings -> Secrets and variables -> Actions
2. Click "New repository secret"
3. Name it (e.g., `DOCKER_PASSWORD`) and paste the value
4. Save

#### Using Secrets in Workflows
```yaml
steps:
  - name: Log in to Docker Hub
    uses: docker/login-action@v3
    with:
      username: ${{ secrets.DOCKER_USERNAME }}
      password: ${{ secrets.DOCKER_PASSWORD }}

  - name: Deploy to server
    env:
      SSH_KEY: ${{ secrets.SERVER_SSH_KEY }}
      SERVER_HOST: ${{ secrets.SERVER_HOST }}
    run: |
      echo "$SSH_KEY" > /tmp/ssh_key
      chmod 600 /tmp/ssh_key
      ssh -i /tmp/ssh_key user@$SERVER_HOST "./deploy.sh"

  - name: Push to AWS ECR
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      AWS_REGION: us-east-1
    run: |
      aws ecr get-login-password --region $AWS_REGION \
        | docker login --username AWS --password-stdin \
          ${{ secrets.ECR_REGISTRY }}
```

> IMPORTANT: If you accidentally print a secret with `echo`, GitHub will redact it in the logs as `***`. But still avoid printing secrets — the redaction is not foolproof.

### Built-in GitHub Context Variables

GitHub provides many pre-defined variables via the `github` context:

| Variable | Value | Example |
|----------|-------|---------|
| `github.sha` | Full commit SHA | `a81bef2c...` |
| `github.ref` | Branch/tag ref | `refs/heads/main` |
| `github.ref_name` | Branch or tag name | `main` |
| `github.event_name` | Trigger type | `push`, `pull_request` |
| `github.actor` | Username that triggered | `john-doe` |
| `github.repository` | `owner/repo` | `myorg/myapp` |
| `github.run_number` | Sequential run count | `42` |
| `github.run_id` | Unique run ID | `12345678` |
| `github.workspace` | Path to checked-out repo | `/home/runner/work/...` |

```yaml
steps:
  - name: Tag Docker image with commit SHA
    run: |
      docker build -t my-app:${{ github.sha }} .
      docker tag my-app:${{ github.sha }} my-app:latest
      echo "Built image tagged: my-app:${{ github.sha }}"

  - name: Only deploy on main branch
    if: github.ref_name == 'main'
    run: ./deploy.sh

  - name: Print context info
    run: |
      echo "Branch: ${{ github.ref_name }}"
      echo "Commit: ${{ github.sha }}"
      echo "Actor: ${{ github.actor }}"
      echo "Run #: ${{ github.run_number }}"
```

### Environment-Specific Deployments with GitHub Environments

GitHub supports named **Environments** (Settings -> Environments) with protection rules:

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production                    # links to the GitHub Environment
      url: https://myapp.example.com      # shown in UI after deploy
    steps:
      - run: ./deploy.sh production
```

Environments can require manual approval before the job runs — useful for production gates.

### Practice Exercise

You have these values to handle:
- Database password — sensitive, must be a secret
- App version — derived from git tag (use `github.ref_name`)
- Deploy target URL — different per branch (main = prod, develop = staging)
- API base URL — not sensitive, same in all jobs

Write the `env:` blocks and secrets references you would need in a deploy workflow.


---

## Lesson 7: Strategy Matrix — Parallel Testing

### Learning Objectives
- Use a matrix to run one job across many configurations simultaneously
- Combine multiple matrix dimensions
- Exclude specific combinations and allow failures on certain matrix entries

### Concept

A **strategy matrix** lets a single job definition fan out into multiple parallel runs — one for each combination of values in the matrix. This is the standard way to test across multiple Python versions, Node.js versions, or operating systems.

### Basic Matrix

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - run: pip install -r requirements.txt
      - run: pytest
```

This creates 4 parallel jobs — one per Python version. All 4 must pass for the workflow to succeed.

### Multi-Dimensional Matrix

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11"]
    os: [ubuntu-latest, windows-latest, macos-latest]
    database: [sqlite, postgres]
```

This produces 2 x 3 x 2 = **12 parallel jobs**. Use this to guarantee your code works in all combinations.

Reference matrix values in steps:
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}          # use matrix value as the runner!
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest
        env:
          CI_OS: ${{ matrix.os }}
```

### Excluding Specific Combinations

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.10", "3.11"]
    exclude:
      - os: windows-latest
        python-version: "3.10"    # skip this specific combination
```

### Including Extra Combinations

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11"]
    include:
      - python-version: "3.12"           # add an extra config
        experimental: true               # custom extra variable
      - python-version: "3.11"
        extra-flag: "--extra-checks"     # add a variable to an existing config
```

### Allow Specific Failures Without Failing the Whole Workflow

```yaml
strategy:
  fail-fast: false             # default: true (stop all on first failure)
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
    include:
      - python-version: "3.12"
        experimental: true

steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
  - run: pytest
    continue-on-error: ${{ matrix.experimental == true }}
```

`fail-fast: false` means all matrix jobs run to completion even if one fails.
`continue-on-error: true` lets this specific job pass even if the step fails.

### Practice Exercise

Write a matrix strategy that:
1. Tests on Python 3.10 and 3.11
2. Tests on both Ubuntu and macOS
3. Excludes the combination of Python 3.10 on macOS
4. Also tests Python 3.12 on Ubuntu only, marking it as experimental
5. Uses `fail-fast: false` so all jobs complete even if one fails

---

## Lesson 8: Artifacts & Dependency Caching

### Learning Objectives
- Upload and download build artifacts between jobs
- Cache dependencies to speed up workflows dramatically

### Part A — Artifacts

**Artifacts** are files produced by a workflow that you want to save. Use cases:
- Test reports / coverage HTML
- Built binaries or wheels
- Docker build logs
- Trained model files

#### Uploading Artifacts
```yaml
steps:
  - name: Run tests with coverage report
    run: pytest --cov=src --cov-report=html:coverage-html

  - name: Upload coverage report
    uses: actions/upload-artifact@v4
    with:
      name: coverage-report          # display name in GitHub UI
      path: coverage-html/           # what to upload
      retention-days: 30             # how long to keep it (default: 90)
    if: always()                     # upload even if tests fail
```

#### Downloading Artifacts in Another Job
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest --cov=src --cov-report=xml
      - uses: actions/upload-artifact@v4
        with:
          name: test-coverage
          path: coverage.xml

  publish-coverage:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: test-coverage
          path: ./coverage

      - name: Publish coverage to Codecov
        run: bash <(curl -s https://codecov.io/bash) -f ./coverage/coverage.xml
```

### Part B — Dependency Caching

Without caching, every workflow run re-downloads all packages from scratch.
With caching, the first run is slow but subsequent runs reuse the cached packages — often saving 1-3 minutes per run.

#### Python (pip) Caching

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    cache: "pip"              # built-in cache support

# OR use the cache action manually for more control:
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

The **cache key** is the secret: `hashFiles('**/requirements.txt')` changes the key whenever `requirements.txt` changes, forcing a cache refresh. Otherwise, the old cache is reused.

#### Node.js (npm) Caching
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm"

# OR manual:
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

#### Docker Layer Caching
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push Docker image
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: my-app:latest
    cache-from: type=gha          # read cache from GitHub Actions cache
    cache-to: type=gha,mode=max   # write cache to GitHub Actions cache
```

### Practice Exercise

Add caching and artifact upload to this workflow:

```yaml
name: Python CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          # TODO: add pip caching here
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=html:coverage/
      # TODO: upload coverage/ as an artifact named "coverage-html"
      # TODO: make sure the artifact is uploaded even when tests fail
```


---

## Lesson 9: Building a Full CI Pipeline

### Learning Objectives
- Build a complete, production-ready CI pipeline for a Python project
- Structure jobs for linting, testing, and building

### Concept

A **CI (Continuous Integration) pipeline** automatically verifies every code change before it can be merged. A good CI pipeline catches bugs early, enforces code quality, and gives the team confidence.

### Full Python CI Pipeline

```yaml
name: Python CI

on:
  push:
    branches: ["main", "develop"]
  pull_request:
    branches: ["main"]

jobs:
  # Job 1: Code quality checks (runs in parallel with tests)
  lint:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install linting tools
        run: pip install flake8 black isort mypy

      - name: Check formatting (black)
        run: black --check src/ tests/

      - name: Check import ordering (isort)
        run: isort --check-only src/ tests/

      - name: Lint (flake8)
        run: flake8 src/ tests/ --max-line-length=88

      - name: Type check (mypy)
        run: mypy src/

  # Job 2: Run tests across multiple Python versions
  test:
    name: Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=xml:coverage.xml \
            --cov-report=html:coverage-html \
            --cov-fail-under=80 \
            -v

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-py${{ matrix.python-version }}
          path: coverage-html/
          retention-days: 14

  # Job 3: Security scan (runs in parallel)
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install security scanner
        run: pip install bandit safety

      - name: Scan for security issues (bandit)
        run: bandit -r src/ -ll

      - name: Check dependencies for known vulnerabilities
        run: safety check -r requirements.txt

  # Job 4: Build Docker image (only after lint and tests pass)
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build image (test build, no push)
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: my-app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Key Design Decisions Explained

| Decision | Why |
|----------|-----|
| `lint` and `test` run in parallel | Saves time — no dependency between them |
| `fail-fast: false` in matrix | All Python versions complete even if one fails |
| `if: always()` on artifact upload | Coverage uploads even when tests fail (so you can see what was covered) |
| `needs: [lint, test, security]` on build | Docker image only built if ALL quality gates pass |
| `--cov-fail-under=80` | CI fails if test coverage drops below 80% |

### Project File Structure for This Pipeline

```
my-project/
├── .github/
│   └── workflows/
│       └── ci.yml          <- the workflow file above
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
├── Dockerfile
├── requirements.txt
└── setup.cfg               <- configure flake8, mypy, isort here
```

### `setup.cfg` for Tool Configuration
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503

[mypy]
ignore_missing_imports = True

[isort]
profile = black
```

### Practice Exercise

1. Create the project structure above
2. Write a simple `calculator.py` with at least 3 functions
3. Write tests with at least 80% coverage
4. Create the CI workflow
5. Push to GitHub and watch all 4 jobs run
6. Intentionally break a test — confirm the CI fails
7. Fix it and confirm CI goes green again


---

## Lesson 10: Building a CD Pipeline — Auto Deployment

### Learning Objectives
- Build a CD workflow that deploys after a successful merge
- Push Docker images to a registry and deploy to a server
- Use environment-based deployment gates

### Concept

**CD (Continuous Deployment/Delivery)** automatically ships your verified code to an environment after CI passes. A typical flow:

```
Code merged to main
        |
        v
CI pipeline passes (tests, lint, security)
        |
        v
Docker image built and tagged
        |
        v
Image pushed to private registry (ECR/Docker Hub)
        |
        v
Deployment triggered on server (pull & restart)
```

### Full CD Workflow — Docker + AWS ECR + SSH Deploy

```yaml
name: Build and Deploy

on:
  push:
    branches: ["main"]     # only deploy on merge to main

jobs:
  # ---- CI gate: must pass before deploy ----
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest

  # ---- Build and push Docker image ----
  build-and-push:
    name: Build & Push Image
    runs-on: ubuntu-latest
    needs: test                           # only runs after tests pass
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}

    steps:
      - uses: actions/checkout@v4

      - name: Generate image metadata and tags
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ secrets.ECR_REGISTRY }}/my-app
          tags: |
            type=sha                      # tag with commit SHA
            type=ref,event=branch         # tag with branch name
            type=raw,value=latest,enable=${{ github.ref_name == 'main' }}

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Log in to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ---- Deploy to staging ----
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-and-push
    environment:
      name: staging
      url: https://staging.myapp.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging server via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /opt/myapp
            aws ecr get-login-password --region ${{ secrets.AWS_REGION }} \
              | docker login --username AWS --password-stdin \
                ${{ secrets.ECR_REGISTRY }}
            docker compose pull
            docker compose up -d --no-build
            docker system prune -f

  # ---- Deploy to production (requires manual approval in GitHub) ----
  deploy-prod:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production                   # configured with required reviewers in Settings
      url: https://myapp.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/myapp
            aws ecr get-login-password --region ${{ secrets.AWS_REGION }} \
              | docker login --username AWS --password-stdin \
                ${{ secrets.ECR_REGISTRY }}
            docker compose pull
            docker compose up -d --no-build
            docker system prune -f
```

### Setting Up GitHub Environments with Protection Rules

1. Go to repo **Settings** -> **Environments** -> **New environment**
2. Name it `production`
3. Under **Protection rules**, add **Required reviewers** (your team members)
4. Optionally enable **Wait timer** (e.g., wait 5 minutes before allowing deployment)
5. Now any workflow referencing `environment: production` will pause and wait for human approval

### docker-compose.yml on the Server

The server only needs a compose file that pulls images — it doesn't build:

```yaml
# /opt/myapp/docker-compose.yml on the server
version: '3'
services:
  app:
    image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=mongodb
      - DB_PASSWORD_FILE=/run/secrets/db_password
    depends_on:
      - mongodb

  mongodb:
    image: mongo:6
    volumes:
      - mongo-data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD_FILE=/run/secrets/db_password

volumes:
  mongo-data:
```

### Required GitHub Secrets for This Pipeline

| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_REGION` | e.g., `us-east-1` |
| `ECR_REGISTRY` | e.g., `123456789.dkr.ecr.us-east-1.amazonaws.com` |
| `STAGING_HOST` | staging server IP or hostname |
| `STAGING_USER` | SSH username on staging server |
| `STAGING_SSH_KEY` | private SSH key for staging |
| `PROD_HOST` | production server IP or hostname |
| `PROD_USER` | SSH username on prod server |
| `PROD_SSH_KEY` | private SSH key for prod |

### Practice Exercise
1. Create a GitHub Environment called `staging` with no protection rules
2. Create a GitHub Environment called `production` with yourself as a required reviewer
3. Write the CD workflow above (use a dummy `echo` command instead of real SSH for now)
4. Push to `main` and watch the pipeline stop at `deploy-prod` waiting for your approval
5. Approve it and verify `deploy-prod` completes


---

## Lesson 11: Reusable Workflows & Composite Actions

### Learning Objectives
- Create a reusable workflow callable from other workflows
- Build a composite action to share steps across jobs

### Part A — Reusable Workflows

A **reusable workflow** is a complete workflow file that other workflows can call — avoiding copy-paste of the same jobs across many workflows.

#### Creating a Reusable Workflow (.github/workflows/reusable-test.yml)
```yaml
name: Reusable - Run Tests

on:
  workflow_call:                     # this makes it callable
    inputs:
      python-version:
        description: "Python version to test with"
        required: false
        default: "3.11"
        type: string
      coverage-threshold:
        required: false
        default: 80
        type: number
    secrets:
      CODECOV_TOKEN:                 # secrets must be explicitly declared
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
          cache: "pip"

      - run: pip install -r requirements.txt pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=src \
            --cov-report=xml \
            --cov-fail-under=${{ inputs.coverage-threshold }}
```

#### Calling the Reusable Workflow
```yaml
name: CI

on:
  push:
    branches: ["main"]

jobs:
  run-tests:
    uses: ./.github/workflows/reusable-test.yml    # local file
    with:
      python-version: "3.11"
      coverage-threshold: 85
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  # You can also call workflows from OTHER repos
  run-shared-tests:
    uses: myorg/shared-workflows/.github/workflows/test.yml@main
    with:
      python-version: "3.10"
    secrets: inherit               # pass all secrets through automatically
```

### Part B — Composite Actions

A **composite action** bundles multiple steps into a single reusable action stored in your repo.

#### Creating a Composite Action (.github/actions/setup-project/action.yml)
```yaml
name: Setup Project
description: Install Python and all project dependencies

inputs:
  python-version:
    description: "Python version"
    required: false
    default: "3.11"

outputs:
  cache-hit:
    description: "Whether the pip cache was hit"
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: "composite"
  steps:
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
        cache: "pip"

    - name: Install dependencies
      shell: bash
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
```

#### Using the Composite Action in Any Workflow
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup project
        uses: ./.github/actions/setup-project      # local composite action
        with:
          python-version: "3.11"

      - run: pytest
```

### When to Use What

| Scenario | Use |
|----------|-----|
| Share entire job sequences across repos | Reusable Workflow (`workflow_call`) |
| Share a group of steps within a job | Composite Action |
| Share a single command or small script | Shell function or a shared script file |
| Use a well-known community tool | Marketplace Action (`uses: owner/repo@v1`) |

### Practice Exercise
1. Extract the "setup Python + install deps" steps from your CI workflow into a composite action at `.github/actions/setup-python-project/action.yml`
2. Use that composite action in your main CI workflow
3. Bonus: extract the entire test job into a reusable workflow and call it from CI

---

## Lesson 12: Real-World MLOps CI/CD Workflow

### Learning Objectives
- Apply GitHub Actions to a machine learning project
- Automate model training, evaluation, and deployment checks

### Concept

CI/CD for ML projects is the same as for software — but the "tests" include model quality gates:
- Does the model still achieve accuracy above a threshold?
- Did data quality degrade?
- Are inference latency requirements met?

### MLOps Pipeline Example

```yaml
name: MLOps CI/CD

on:
  push:
    branches: ["main"]
    paths:
      - "src/**"
      - "data/**"
      - "models/**"
      - "requirements.txt"
  pull_request:
    branches: ["main"]
  schedule:
    - cron: "0 2 * * 1"       # Weekly retrain check every Monday 2AM

jobs:
  # ---- Code quality ----
  lint-and-test:
    name: Code Quality & Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install flake8 pytest pytest-cov

      - name: Lint
        run: flake8 src/

      - name: Unit tests (data processing, feature engineering)
        run: pytest tests/unit/ -v

  # ---- Model training & evaluation ----
  train-and-evaluate:
    name: Train & Evaluate Model
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install ML dependencies
        run: pip install -r requirements.txt

      - name: Train model on validation set
        run: python src/train.py --mode=ci --data=data/validation/
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          MLFLOW_EXPERIMENT_NAME: ci-validation

      - name: Evaluate model quality gates
        run: |
          python src/evaluate.py \
            --min-accuracy=0.85 \
            --max-latency-ms=200 \
            --output=evaluation_results.json

      - name: Upload evaluation results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: model-evaluation
          path: evaluation_results.json

      - name: Post evaluation summary to PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('evaluation_results.json'));
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Model Evaluation Results\n\n` +
                    `- Accuracy: ${results.accuracy}\n` +
                    `- F1 Score: ${results.f1_score}\n` +
                    `- Avg Latency: ${results.avg_latency_ms}ms\n` +
                    `- Status: ${results.passed ? 'PASSED' : 'FAILED'}`
            });

  # ---- Build inference Docker image ----
  build-inference-image:
    name: Build Inference Service
    runs-on: ubuntu-latest
    needs: train-and-evaluate
    if: github.ref_name == 'main'

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push inference image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.inference
          push: true
          tags: |
            ${{ secrets.ECR_REGISTRY }}/ml-inference:latest
            ${{ secrets.ECR_REGISTRY }}/ml-inference:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ---- Deploy inference service ----
  deploy-inference:
    name: Deploy Inference Service
    runs-on: ubuntu-latest
    needs: build-inference-image
    environment:
      name: production-ml
      url: https://api.myml.example.com

    steps:
      - name: Update inference service on server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.ML_SERVER_HOST }}
          username: ${{ secrets.ML_SERVER_USER }}
          key: ${{ secrets.ML_SERVER_SSH_KEY }}
          script: |
            cd /opt/ml-inference
            docker compose pull
            docker compose up -d --no-build
            # Run smoke test
            sleep 10
            curl -f http://localhost:8080/health || exit 1
            echo "Deployment successful"
```

### Key MLOps Pipeline Patterns

| Pattern | How |
|---------|-----|
| Model quality gate | `evaluate.py` fails with exit code 1 if accuracy drops below threshold |
| PR comment with results | `actions/github-script` posts evaluation metrics to the PR |
| Artifact tracking | Upload `evaluation_results.json` as a workflow artifact |
| Tag-based versioning | `docker/metadata-action` creates tags from git SHA and branch |
| Smoke test after deploy | `curl -f` checks the health endpoint returns 200 |

### Practice Exercise

Adapt the pipeline for your project:
1. Replace `src/train.py` with your actual training script
2. Replace the accuracy threshold with your model's minimum acceptable performance metric
3. Add a step that checks the model file size is below a deployment limit (e.g., `du -sh model.pkl`)
4. Add a data validation step using `great_expectations` or simple Python assertions


---

## Lesson 13: Debugging & Common Pitfalls

### Learning Objectives
- Diagnose and fix the most common GitHub Actions errors
- Use debugging tools built into GitHub Actions

### Common Errors and Fixes

#### 1. Workflow Does Not Trigger

**Symptom:** You push code but nothing appears in the Actions tab.

| Cause | Fix |
|-------|-----|
| Branch name mismatch | Check `on: push: branches:` — is it `main` or `master`? |
| Wrong file location | Workflow must be in `.github/workflows/` (two levels deep) |
| YAML syntax error | GitHub silently ignores invalid YAML — use a YAML validator |
| `paths-ignore` is too broad | Your push matches the ignore filter |

```yaml
# Common mistake: workflow file in wrong location
.github/ci.yml              # WRONG - GitHub won't detect this
.github/workflows/ci.yml    # CORRECT
```

#### 2. ModuleNotFoundError / Command Not Found

**Symptom:** A step fails with `ModuleNotFoundError: No module named 'pandas'`

```yaml
# WRONG: forgot to install dependencies before using them
steps:
  - uses: actions/checkout@v4
  - run: pytest                         # fails - nothing is installed

# CORRECT: install first
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.11"
  - run: pip install -r requirements.txt   # install BEFORE running
  - run: pytest
```

> Each job starts in a completely empty VM. Nothing from your local machine or another job carries over automatically.

#### 3. "Works on My Machine" but Fails in CI

**Symptom:** Tests pass locally but fail in the CI runner.

Common causes:
- Package missing from `requirements.txt` (installed globally on your machine)
- Hardcoded local file path (e.g., `/Users/john/data/`)
- Environment variable not set in CI
- Different OS behavior (Windows vs Linux line endings)

**Debug approach:**
```yaml
- name: Debug environment
  run: |
    python --version
    pip list
    env | sort
    ls -la
    pwd
```

#### 4. YAML Indentation Error

GitHub Actions YAML is indentation-sensitive. Tabs vs spaces will break it silently or with cryptic errors.

```yaml
# WRONG - tab indentation
jobs:
	test:           # <- TAB character here causes parse error
		runs-on: ubuntu-latest

# CORRECT - 2 spaces per indent level
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

Use a YAML validator or VS Code with the YAML extension to catch these before pushing.

#### 5. Secrets Not Available / Empty

**Symptom:** Step fails with "Authentication failed" or the secret value is empty.

Checklist:
- [ ] Secret name spelling matches exactly (case-sensitive)
- [ ] Secret is added to the correct repo (not just org-level)
- [ ] For PRs from forks: secrets are NOT passed to forked PRs by default (security feature)
- [ ] Secret is not expired or rotated without updating GitHub

```yaml
# Verify a secret is set (do NOT print the actual value)
- name: Check secret is available
  run: |
    if [ -z "${{ secrets.MY_SECRET }}" ]; then
      echo "ERROR: MY_SECRET is empty or not set"
      exit 1
    fi
    echo "Secret is set (length: ${#MY_SECRET})"
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}
```

#### 6. Job Fails but Workflow Shows Green

**Symptom:** A step exits with an error but the workflow still reports success.

Cause: `continue-on-error: true` was set on a critical step, or a script exits with code 0 even on failure.

```yaml
# Dangerous: hides failures
- run: ./run-tests.sh || true        # WRONG - always exits 0

# Correct: let failures propagate
- run: ./run-tests.sh                # exit code propagates to workflow
```

#### 7. Docker Build Fails in CI

```yaml
# Common fix: ensure Docker Buildx is set up before building
steps:
  - uses: actions/checkout@v4

  - name: Set up Docker Buildx           # REQUIRED for advanced builds
    uses: docker/setup-buildx-action@v3

  - name: Build image
    uses: docker/build-push-action@v6
    with:
      context: .
      push: false
      tags: my-app:test
```

#### 8. Caching Not Working

**Symptom:** Cache is never restored — every run installs packages from scratch.

Cause: The cache key changes on every run.

```yaml
# WRONG: uses github.sha - unique every commit, so cache never hits
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ github.sha }}

# CORRECT: key is stable unless requirements.txt changes
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Enabling Debug Logging

Add these GitHub Actions secrets to enable verbose logging:
- Secret name: `ACTIONS_STEP_DEBUG`, value: `true`
- Secret name: `ACTIONS_RUNNER_DEBUG`, value: `true`

Or trigger with the debug flag via API/CLI:
```bash
gh workflow run ci.yml --ref main -f debug=true
```

### Using `tmate` for SSH Debugging (Interactive Session)

When a workflow is failing and logs aren't enough, you can SSH into the runner:

```yaml
- name: Setup tmate session (interactive debug)
  uses: mxschmitt/action-tmate@v3
  if: failure()                     # only on failure
  with:
    limit-access-to-actor: true     # only you can connect
```

This pauses the workflow and gives you an SSH command to connect to the live runner. You can then manually run commands to debug.

### Workflow Run Re-run Options

In the GitHub UI under the Actions tab:
- **Re-run all jobs** — restart from scratch
- **Re-run failed jobs** — only re-run the jobs that failed (saves time)
- **Re-run with debug logging** — re-run with full verbose output

### Quick Debugging Checklist

When a workflow fails:
- [ ] Check the red step in the Actions UI — click to expand the logs
- [ ] Look for the actual error message (often buried in output)
- [ ] Check that all `secrets.*` references exist in repo settings
- [ ] Check that branch names in `on:` match your actual branch
- [ ] Validate your YAML at yaml-online-parser.appspot.com
- [ ] Add `echo` debug statements to trace what variables contain
- [ ] Check the runner's OS matches what you expect
- [ ] Verify the action version (`@v4`) is not deprecated


---

## Quick Reference Cheat Sheet

### Workflow File Location
```
your-repo/
└── .github/
    └── workflows/
        ├── ci.yml         <- triggered on push/PR
        ├── deploy.yml     <- triggered on merge to main
        └── nightly.yml    <- triggered on schedule
```

### Trigger Syntax

```yaml
on:
  push:
    branches: ["main", "develop"]
    paths: ["src/**"]
  pull_request:
    branches: ["main"]
    types: [opened, synchronize]
  schedule:
    - cron: "0 6 * * 1-5"
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]
  workflow_call:            # makes this workflow reusable
```

### Job Structure

```yaml
jobs:
  my-job:
    runs-on: ubuntu-latest
    needs: [other-job]             # dependency
    if: github.ref_name == 'main'  # conditional
    environment: production        # env gate with approval
    outputs:
      my-output: ${{ steps.step-id.outputs.value }}
    env:
      MY_VAR: hello
    steps:
      - name: Step name
        uses: actions/checkout@v4
      - name: Another step
        run: echo "hello"
```

### Useful Context Variables

```yaml
${{ github.sha }}               # commit SHA
${{ github.ref_name }}          # branch name (main, develop)
${{ github.event_name }}        # push, pull_request, schedule
${{ github.actor }}             # who triggered
${{ github.repository }}        # owner/repo
${{ github.run_number }}        # sequential run count
${{ runner.os }}                # Linux, Windows, macOS
${{ matrix.python-version }}    # matrix variable
${{ steps.my-step.outputs.x }}  # step output
${{ needs.my-job.outputs.x }}   # job output
${{ secrets.MY_SECRET }}        # encrypted secret
${{ inputs.my-input }}          # workflow_dispatch / workflow_call input
```

### Commonly Used Actions

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with: { python-version: "3.11", cache: "pip" }
- uses: actions/setup-node@v4
  with: { node-version: "20", cache: "npm" }
- uses: actions/upload-artifact@v4
  with: { name: my-artifact, path: dist/ }
- uses: actions/download-artifact@v4
  with: { name: my-artifact }
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
- uses: docker/login-action@v3
- uses: docker/build-push-action@v6
- uses: aws-actions/configure-aws-credentials@v4
- uses: aws-actions/amazon-ecr-login@v2
- uses: docker/metadata-action@v5
```

### Strategy Matrix

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
    os: [ubuntu-latest, windows-latest]
    exclude:
      - os: windows-latest
        python-version: "3.10"

runs-on: ${{ matrix.os }}    # use matrix value as runner
python-version: ${{ matrix.python-version }}
```

### Secrets vs Environment Variables

```yaml
# Secrets (encrypted, never shown in logs)
password: ${{ secrets.DB_PASSWORD }}

# Environment variables (plain text, visible in logs)
env:
  APP_ENV: production
  LOG_LEVEL: debug
```

### Conditional Step Execution

```yaml
# Run only on main branch
if: github.ref_name == 'main'

# Run only on push events (not PR)
if: github.event_name == 'push'

# Always run (even if previous step failed)
if: always()

# Run only if previous step failed
if: failure()

# Run only if previous step succeeded (default behavior)
if: success()

# Run for experimental matrix entry even on failure
continue-on-error: ${{ matrix.experimental == true }}
```

### Artifact Upload/Download

```yaml
# Upload
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results
    path: reports/
    retention-days: 30

# Download in another job
- uses: actions/download-artifact@v4
  with:
    name: test-results
    path: ./reports
```

### Job Outputs

```yaml
jobs:
  producer:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.ver.outputs.version }}
    steps:
      - id: ver
        run: echo "version=1.2.3" >> $GITHUB_OUTPUT

  consumer:
    needs: producer
    runs-on: ubuntu-latest
    steps:
      - run: echo "Version is ${{ needs.producer.outputs.version }}"
```

---

## Full Workflow Templates

### Minimal Python CI

```yaml
name: Python CI
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest
```

### CI + Docker Build + Push to ECR

```yaml
name: CI and Build
on:
  push:
    branches: ["main"]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install -r requirements.txt && pytest

  build-push:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - uses: aws-actions/amazon-ecr-login@v2
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ secrets.ECR_REGISTRY }}/my-app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Multi-Version Matrix Test

```yaml
name: Matrix CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
```

---

## Further Learning Resources

| Topic | Resource |
|-------|----------|
| GitHub Actions Official Docs | https://docs.github.com/en/actions |
| Workflow syntax reference | https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions |
| GitHub Marketplace (Actions) | https://github.com/marketplace?type=actions |
| Cron expression helper | https://crontab.guru |
| YAML validator | https://yaml-online-parser.appspot.com |
| docker/metadata-action | https://github.com/docker/metadata-action |
| aws-actions collection | https://github.com/aws-actions |

---

*Lesson guide for GitHub Actions CI/CD. Complete every practice exercise to build hands-on confidence.*
*Pair this guide with the Docker lesson for a complete understanding of containerized CI/CD pipelines.*
