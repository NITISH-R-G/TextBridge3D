from __future__ import annotations

from fastapi import FastAPI

from app.generators import generate_mesh
from app.schemas import GenerateRequest, GenerateResponse


app = FastAPI(
    title="Text-to-3D Demo Backend",
    version="0.1.0",
    description="A simple FastAPI backend that simulates text-to-3D generation.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    return generate_mesh(request.prompt)
