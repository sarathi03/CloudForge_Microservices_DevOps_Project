# CloudForge Architecture

## Services

### Frontend
Provides the web interface used by application users.

### Backend
Exposes REST APIs and handles application business logic.

### Worker
Processes background tasks independently from the API request flow.

### PostgreSQL
Stores application data persistently.

## High-Level Flow

User
 |
 v
Frontend
 |
 v
Backend API --------> Worker
 |
 v
PostgreSQL

## Container Networking

The services will communicate over a private Docker Compose network.
The backend will connect to PostgreSQL using the Compose service name.

## Deployment

Jenkins will automate testing, Docker image builds, image tagging,
publishing to Amazon ECR, and the approved deployment workflow.

## Security

- Do not commit secrets to Git.
- Keep database access private.
- Restrict inbound network rules.
- Use least-privilege IAM permissions.
- Verify service health after deployment.
