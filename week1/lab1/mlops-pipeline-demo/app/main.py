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
    """Cloud Run / load balancers ping this to check the container is alive."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(payload: PredictRequest) -> PredictResponse:
    return PredictResponse(result=predict(payload.value))
