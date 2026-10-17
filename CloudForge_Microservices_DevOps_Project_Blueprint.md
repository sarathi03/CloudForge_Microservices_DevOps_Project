# Project Blueprint: CloudForge — Microservices CI/CD Platform

> **Purpose:** Complete learning and implementation blueprint for a brand-new DevOps project built from zero.  
> **Project name:** **CloudForge**  
> **Status:** Planning only — no infrastructure has been created yet.  
> **Learning style:** One step at a time. Understand each command, verify the result, then continue.

## 1. Project overview

**CloudForge** is a containerized multi-service application with an automated CI/CD pipeline. We will create the application code, Git configuration, Docker images, AWS ECR repositories, Jenkins pipeline, deployment configuration, and monitoring from scratch.

We will learn to:
1. Build a small application split into services with clear responsibilities.
2. Containerize each custom service.
3. Run the stack locally with Docker Compose, private networking, DNS, and persistent storage.
4. Store images in separate Amazon ECR repositories.
5. Tag images with release versions and Git commit identifiers.
6. Use Jenkins to test, build, tag, push, and deploy images.
7. Deploy to a newly prepared AWS environment.
8. Add health checks, security controls, logging, image lifecycle policies, rollback planning, and cleanup documentation.

**Isolation rule:** We will not reuse or modify the existing `Automated-CICD-Pipeline-for-a-Python-Application` project, its Jenkins job, ECR repository, EC2 host, IAM role, security groups, or deployment setup. Everything for CloudForge will be newly created when we reach the relevant phase.

## 2. Project 1 vs Project 2

| Area | Project 1: `Automated-CICD-Pipeline-for-a-Python-Application` | Project 2: `CloudForge` |
|---|---|---|
| Main goal | Learn the basic CI/CD flow | Practice a multi-service, real-world DevOps workflow |
| Application | One small Python HTTP application | Frontend, backend/API, and worker with separate responsibilities |
| Database | No dedicated database in the basic app | PostgreSQL for persistent application data |
| Dockerfiles | One application Dockerfile | One Dockerfile per custom service; PostgreSQL can use its official image |
| Networking | Basic host-to-container port access | Private container network and service-name DNS |
| Image registry | One ECR repository for the demo image | Separate ECR repository for each custom service |
| Versioning | Basic tags such as `latest` and build number | Release tag such as `v1.0.0` plus Git commit tag |
| CI/CD | One app build/push/deploy flow | Test/build/tag/push per service, followed by deployment |
| Deployment | Simple container deployment | Compose-based multi-container deployment on a new host initially |
| Reliability | Basic health endpoint check | Service health checks, deployment verification, rollback plan |
| Security | Basic ECR access | Least-privilege IAM, protected configuration, restricted database access |
| Operations | Manual troubleshooting | Logs, lifecycle policies, troubleshooting and cleanup documentation |
| Infrastructure | Existing practice environment | Freshly planned resources created only when needed |

Having multiple containers alone does not automatically make an application good microservices architecture. Each service should have a clear responsibility and be independently buildable and deployable.

## 3. Proposed architecture

### Services

1. **Frontend** — a simple web UI that calls the backend API.
2. **Backend/API** — handles requests and business logic; reads/writes application data in PostgreSQL.
3. **Worker** — performs a background task separately from request handling. We will implement a real, observable task rather than an empty container.
4. **PostgreSQL** — stores application data. We will initially use the official PostgreSQL image and keep credentials out of source control.

We may add a message broker later if it improves the worker example. We will avoid adding technologies just to make the architecture look complicated.

### High-level flow

```text
Developer
   |
   v
New GitHub repository: cloudforge-microservices-platform
   |
   v
Jenkins CI/CD
   |-- Checkout source
   |-- Run tests
   |-- Build service images
   |-- Tag images (release + Git commit)
   |-- Authenticate to Amazon ECR
   |-- Push to service-specific ECR repositories
   |
   v
Amazon ECR (private registry)
   |-- cloudforge-frontend
   |-- cloudforge-backend
   |-- cloudforge-worker
   |
   v
New AWS deployment host
   |-- Pull approved image tags
   |-- Docker Compose starts services
   |-- Docker network connects containers
   |-- Health checks verify deployment
   |
   v
Frontend -> Backend/API -> PostgreSQL
                    |
                    v
                  Worker
```

The exact frontend-to-backend route, worker job flow, and network boundaries will be finalized during design. This diagram shows the intended direction, not infrastructure that already exists.

## 4. Naming and versioning conventions

### GitHub and local folder
- GitHub repository: `cloudforge-microservices-platform`
- Local folder: `cloudforge/`

### ECR repositories
- `cloudforge-frontend`
- `cloudforge-backend`
- `cloudforge-worker`

Each repository can contain multiple image tags. PostgreSQL will use the official upstream image initially, so it does not need a custom ECR repository unless we later build a customized database image.

### Example image references

```text
<account-id>.dkr.ecr.<region>.amazonaws.com/cloudforge-backend:v1.0.0
<account-id>.dkr.ecr.<region>.amazonaws.com/cloudforge-backend:git-a1b2c3d
```

These are examples only. We will use the actual AWS account ID, region, and commit hash during implementation.

### Tag policy
- **Release tag:** `v1.0.0`, `v1.1.0`, etc.
- **Git commit tag:** `git-<short-commit-sha>`, to identify the source revision.
- **Optional convenience tag:** `latest`, only if we explicitly choose to maintain it. Deployments should preferably use a specific release or commit tag.
- Do not reuse a Git commit tag for a different image build.
- ECR tag immutability can help prevent accidental overwrites; we will choose settings that fit the release-tag strategy.

## 5. Planned repository layout

We will build this structure gradually instead of creating all files at once.

```text
cloudforge/
├── frontend/
│   ├── Dockerfile
│   ├── source files
│   └── tests/
├── backend/
│   ├── Dockerfile
│   ├── source files
│   └── tests/
├── worker/
│   ├── Dockerfile
│   ├── source files
│   └── tests/
├── tests/
├── compose.yaml
├── Jenkinsfile
├── .dockerignore
├── .gitignore
├── .env.example
├── README.md
└── docs/
    ├── architecture.md
    ├── deployment.md
    ├── troubleshooting.md
    └── cleanup.md
```

We will choose the framework and exact source files before implementation. `compose.yaml` defines how services run together, including networks, ports, volumes, configuration, and health checks. The `Jenkinsfile` orchestrates the pipeline; it does not replace Dockerfiles or Compose.

## 6. Step-by-step implementation roadmap

### Phase 0 — Design and safety
**Goal:** Agree on architecture and plan a clean environment.
- Confirm service responsibilities and application framework.
- Confirm AWS account and region for the new project.
- Plan an AWS budget and billing alerts before creating billable resources.
- Decide resource names and which resources must be new.
- Never paste credentials, secret keys, tokens, or passwords into GitHub or chat.

**Checkpoint:** Architecture, naming, and cost/safety plan are agreed.

### Phase 1 — Create the project locally
**Goal:** Start with a clean directory and a new Git repository.
- Create `cloudforge/`.
- Initialize Git and create a new GitHub repository.
- Add `.gitignore`, `.dockerignore`, and `.env.example`.
- Add the initial README and architecture notes.
- Make the first commit.

**Checkpoint:** A fresh repository exists and contains no secrets or old project configuration.

### Phase 2 — Build application services
**Goal:** Make the application work before containerizing it.
- Implement the frontend.
- Implement the backend API and health endpoint.
- Add PostgreSQL connectivity and a small data operation.
- Implement an observable worker task.
- Add tests and verify each service locally.

**Checkpoint:** Services work locally, tests pass, and responsibilities are clear.

### Phase 3 — Dockerize each custom service
**Goal:** Create repeatable images.
- Write a Dockerfile for each custom service.
- Choose appropriate base images and startup commands.
- Add `.dockerignore` rules to avoid copying unnecessary files or secrets.
- Build each image with a consistent local name.
- Run images and inspect logs, exit codes, and health.

**Checkpoint:** Each custom service image builds and runs.

### Phase 4 — Docker Compose and networking
**Goal:** Run the application as a connected system.
- Define frontend, backend, worker, and PostgreSQL in `compose.yaml`.
- Define a private Compose network.
- Use service names such as `backend` and `postgres` for container-to-container DNS.
- Publish host ports only where required.
- Keep PostgreSQL private by default.
- Configure environment variables and a persistent database volume.
- Add health checks and readiness handling.
- Test requests, database persistence, restarts, and logs.

**Checkpoint:** The stack starts with Compose and services communicate correctly.

### Phase 5 — New AWS ECR setup
**Goal:** Create private repositories for custom service images.
- Confirm AWS account and region.
- Create `cloudforge-frontend`, `cloudforge-backend`, and `cloudforge-worker`.
- Learn repository URIs, tags, digests, permissions, and image scanning settings.
- Choose a tag-immutability strategy.
- Configure lifecycle policies only after defining which versions to retain.
- Use least-privilege IAM permissions for pushing and pulling.

**Checkpoint:** Repositories exist and push/pull permissions are understood.

### Phase 6 — Manual ECR image workflow
**Goal:** Understand ECR commands before automating them.
For each custom service:
1. Build the image locally.
2. Authenticate Docker to ECR using AWS CLI.
3. Tag the image with the full ECR URI.
4. Add a release tag and a Git commit tag.
5. Push both tags.
6. Verify tags and image digest in ECR.
7. Pull the image from ECR.
8. Run the pulled image and test it.
9. Troubleshoot an incorrect repository/tag safely.

**Checkpoint:** We can explain and perform build, tag, push, inspect, and pull without Jenkins.

### Phase 7 — Prepare a new AWS deployment host
**Goal:** Create a separate deployment target.
- Choose a deployment approach suitable for the learning budget.
- If using EC2 first, create a new host, a clearly named security group, and an appropriate instance role.
- Install/configure Docker and required tools.
- Configure ECR pull permissions.
- Restrict inbound traffic to necessary ports and trusted sources.
- Never expose PostgreSQL publicly.
- Verify ECR authentication and image pull.

**Checkpoint:** The new host works independently of the old project's EC2, IAM role, security group, and Jenkins setup.

### Phase 8 — Manual deployment with Compose
**Goal:** Prove deployment before automating it.
- Prepare deployment Compose configuration.
- Configure image URIs/tags and runtime variables.
- Pull approved versions from ECR.
- Start services and run health/end-to-end tests.
- Verify logs, networking, and persistent data.
- Document stop/restart procedures.

**Checkpoint:** The application deploys from ECR using documented commands.

### Phase 9 — New Jenkins CI/CD pipeline
**Goal:** Automate the validated workflow.
- Set up Jenkins in a new environment, or choose a separate controller/agent arrangement.
- Create a new Jenkins job connected to the new GitHub repository.
- Configure credentials or IAM-based access safely.
- Add stages for checkout, tests, image build, tag generation, ECR login, push, deployment, and health verification.
- Start with a simple pipeline; optimize to build only changed services later.
- Add clear logs, failure handling, and source-change triggers.

**Checkpoint:** A code change triggers a pipeline that tests, publishes, and deploys the intended image versions.

### Phase 10 — Release safety and rollback
**Goal:** Practice safer releases.
- Deploy a specific version/commit tag, not just `latest`.
- Keep previous known-good images available.
- Define the response to failed health checks.
- Practice rolling back to a previously verified image.
- Ensure database changes are compatible with rollback.
- Do not delete images still required for rollback.

**Checkpoint:** We can identify the running version and restore a known-good version.

### Phase 11 — Monitoring, security, and lifecycle management
**Goal:** Add operational maturity after the core pipeline works.
- Review logs and service health.
- Add basic monitoring if appropriate.
- Review IAM permissions and exposed ports.
- Keep secrets out of source control and image layers.
- Configure ECR lifecycle policies with an explicit retention plan.
- Review image scan findings and update base images.
- Document troubleshooting.

**Checkpoint:** Health, security, and image retention practices are documented.

### Phase 12 — Documentation and cleanup
**Goal:** Finish a portfolio-ready project and control costs.
- Update README with architecture, setup, and deployment steps.
- Document pipeline stages, example commands, and expected outputs.
- Add troubleshooting and cleanup instructions.
- Stop/delete unneeded billable resources after practice.
- Check EBS volumes, snapshots, public IPv4 addresses, ECR storage, load balancers, and other resources before cleanup.
- Verify cleanup in AWS Console.

**Checkpoint:** The project is documented, demonstrable, and its AWS costs/resources are understood.

## 7. What each file or component does

| File/component | Responsibility |
|---|---|
| `frontend/Dockerfile` | Instructions for building the frontend image |
| `backend/Dockerfile` | Instructions for building the backend image |
| `worker/Dockerfile` | Instructions for building the worker image |
| `compose.yaml` | Runs services together; defines networks, ports, volumes, configuration, and health checks |
| `Jenkinsfile` | Automates CI/CD stages and commands |
| `.dockerignore` | Excludes files from the Docker build context |
| `.gitignore` | Tells Git which files not to track |
| `.env.example` | Documents required variable names without real secrets |
| AWS ECR | Private image storage and tag management |
| IAM roles/policies | Controls AWS permissions for push/pull and other operations |
| EC2, if selected | Host where containers run |
| README and `docs/` | Setup, architecture, troubleshooting, deployment, and cleanup instructions |

**Remember:** Dockerfile does not automatically push images to ECR. Jenkins does not replace Compose. ECR stores images; it does not run the app. EC2/Docker (or a later chosen orchestrator) runs containers.

## 8. ECR versioning example

If a backend source revision has Git commit `a1b2c3d`, we may push:

```text
cloudforge-backend:v1.0.0
cloudforge-backend:git-a1b2c3d
```

Both tags can refer to the same image digest when pushed from the same built image. A later release might use:

```text
cloudforge-backend:v1.1.0
cloudforge-backend:git-e4f5a6b
```

We will verify this in ECR. Tags are references to image manifests; the digest identifies exact image content. Tag immutability and release conventions will be planned together.

## 9. Security and cost guardrails

- Never commit AWS access keys, GitHub tokens, database passwords, `.env` files, or Jenkins secrets.
- Prefer IAM roles for workloads running on AWS instead of long-lived access keys.
- Apply least-privilege ECR push/pull permissions.
- Keep database ports private.
- Expose only required application/administration ports, preferably to trusted source IPs.
- Set AWS Budgets and billing alerts; alerts are not a hard spending cap.
- Use small suitable instances for learning and stop/delete resources when not needed.
- Review EBS volumes, snapshots, Elastic IPs/public IPv4 charges, ECR storage, load balancers, and other billable resources.
- Retain rollback images until they are no longer required.

## 10. Definition of done

- [ ] New source repository is independent of Project 1.
- [ ] Frontend, backend, and worker have clear responsibilities.
- [ ] Custom service images build successfully.
- [ ] Compose networking and service-name DNS work.
- [ ] PostgreSQL data persists across container restarts.
- [ ] Each custom service has its own ECR repository.
- [ ] Release and Git commit tags can be pushed and pulled.
- [ ] New deployment environment pulls and runs approved ECR images.
- [ ] Jenkins tests, builds, tags, pushes, and deploys the services.
- [ ] Health verification and rollback are documented and tested.
- [ ] Secrets are not stored in source control or image layers.
- [ ] README, troubleshooting, and cleanup documentation are complete.
- [ ] Unneeded billable AWS resources are stopped or removed.

## 11. How we will work together

1. We will start only when you say you are ready.
2. We will complete one phase at a time.
3. I will explain every command, file, and AWS setting in simple terms.
4. You will run the step and share the result or error.
5. We will verify it before moving to the next step.
6. We will not assume an AWS resource, repository, Jenkins job, or configuration exists until we create or verify it.
7. If the design changes, we will update this blueprint before proceeding.

**Next action when ready:** Begin Phase 0 by confirming service design, application framework, AWS account/region, and cost guardrails. No AWS resources should be created just by reading this document.
