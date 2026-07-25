from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Secure MLOps API"
)

@app.get("/")
def root():
    return {
        "service": "Enterprise Secure MLOps API",
        "status": "Running"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
