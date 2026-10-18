from fastapi import FastAPI

app = FastAPI(
    title="CloudForge Backend API",
    description="Backend service for the CloudForge platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "cloudforge-backend",
        "message": "CloudForge Backend API is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "cloudforge-backend",
    }
