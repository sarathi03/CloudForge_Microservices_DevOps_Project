# CloudForge — Microservices DevOps Platform

CloudForge is a hands-on project for learning microservices, Docker,
AWS container deployment, and CI/CD automation.

## Architecture

- Frontend: Web user interface
- Backend: REST API and application logic
- Worker: Background task processing
- PostgreSQL: Persistent application database

## Technology Stack

- Git and GitHub
- Python and FastAPI
- React and Vite
- Docker and Docker Compose
- Jenkins
- Amazon ECR
- Amazon EC2
- AWS IAM
- Prometheus and Grafana

## Planned Workflow

1. Develop and test the application services.
2. Build Docker images for each custom service.
3. Run services using Docker Compose.
4. Push versioned images to Amazon ECR.
5. Automate testing and image publishing with Jenkins.
6. Deploy approved images to AWS.
7. Verify service health and document rollback procedures.

## Repository Structure

- frontend/: Frontend application
- backend/: Backend API
- worker/: Background worker
- tests/: Application and integration tests
- docs/: Architecture and operations documentation

## Getting Started

Refer to CloudForge_Microservices_DevOps_Project_Blueprint.md
for the implementation roadmap.

Configuration examples are available in .env.example.
Never commit real credentials, passwords, access keys, or private keys.

## Project Status

Initial repository and EC2 development environment setup in progress.
