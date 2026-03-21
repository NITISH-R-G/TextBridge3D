from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Text prompt for 3D generation.")

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        prompt = value.strip()
        if not prompt:
            raise ValueError("Prompt must not be empty.")
        return prompt


class MaterialProperties(BaseModel):
    name: str
    color: str = Field(..., description="Hex RGB color.")
    roughness: float = Field(..., ge=0.0, le=1.0)
    opacity: float = Field(..., ge=0.0, le=1.0)


class MeshDimensions(BaseModel):
    width: float | None = None
    height: float
    depth: float | None = None
    radius: float | None = None
    segments: int | None = None


class MeshMetadata(BaseModel):
    original_prompt: str
    object_name: str
    generator: str = "rule-based-text-to-3d-demo"


class GenerateResponse(BaseModel):
    shape: Literal["cube", "cylinder"]
    dimensions: MeshDimensions
    vertices: List[List[float]]
    faces: List[List[int]]
    material: MaterialProperties
    meta: MeshMetadata
