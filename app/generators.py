from __future__ import annotations

import math
import re
from dataclasses import dataclass

from app.schemas import GenerateResponse, MaterialProperties, MeshDimensions, MeshMetadata


@dataclass(frozen=True)
class ParsedPrompt:
    shape: str
    size: float
    height: float
    radius: float
    segments: int
    material: MaterialProperties
    object_name: str


def generate_mesh(prompt: str) -> GenerateResponse:
    parsed = parse_prompt(prompt)
    if parsed.shape == "cylinder":
        vertices, faces = generate_cylinder(parsed.radius, parsed.height, parsed.segments)
        dimensions = MeshDimensions(
            height=parsed.height,
            radius=parsed.radius,
            segments=parsed.segments,
        )
    else:
        vertices, faces = generate_cube(parsed.size)
        dimensions = MeshDimensions(
            width=parsed.size,
            height=parsed.size,
            depth=parsed.size,
        )

    return GenerateResponse(
        shape=parsed.shape,
        dimensions=dimensions,
        vertices=vertices,
        faces=faces,
        material=parsed.material,
        meta=MeshMetadata(
            original_prompt=prompt,
            object_name=parsed.object_name,
        ),
    )


def parse_prompt(prompt: str) -> ParsedPrompt:
    lowered = prompt.lower()
    shape = detect_shape(lowered)
    size = extract_number(lowered, fallback=4.0)
    height = extract_dimension(lowered, "height", fallback=max(size * 1.5, 4.0))
    radius = extract_dimension(lowered, "radius", fallback=max(size / 2.0, 1.5))
    segments = max(12, int(extract_dimension(lowered, "segments", fallback=16)))

    return ParsedPrompt(
        shape=shape,
        size=size,
        height=height,
        radius=radius,
        segments=segments,
        material=detect_material(lowered),
        object_name=build_object_name(shape, prompt),
    )


def detect_shape(prompt: str) -> str:
    cylinder_keywords = ("cylinder", "tube", "column", "round", "pipe")
    cube_keywords = ("cube", "box", "block", "square")

    if any(keyword in prompt for keyword in cylinder_keywords):
        return "cylinder"
    if any(keyword in prompt for keyword in cube_keywords):
        return "cube"
    return "cube"


def extract_number(prompt: str, fallback: float) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)", prompt)
    if not match:
        return fallback
    return max(float(match.group(1)), 0.5)


def extract_dimension(prompt: str, label: str, fallback: float) -> float:
    pattern = rf"{label}\s*(?:=|:)?\s*(\d+(?:\.\d+)?)"
    match = re.search(pattern, prompt)
    if not match:
        return fallback
    return max(float(match.group(1)), 0.5)


def detect_material(prompt: str) -> MaterialProperties:
    presets = {
        "glass": MaterialProperties(name="glass", color="#9ad9ff", roughness=0.08, opacity=0.45),
        "metal": MaterialProperties(name="metal", color="#9aa3ad", roughness=0.2, opacity=1.0),
        "wood": MaterialProperties(name="wood", color="#9c6b3f", roughness=0.6, opacity=1.0),
        "red": MaterialProperties(name="matte-red", color="#d94841", roughness=0.75, opacity=1.0),
        "blue": MaterialProperties(name="matte-blue", color="#3d7be0", roughness=0.7, opacity=1.0),
        "green": MaterialProperties(name="matte-green", color="#3f9d5c", roughness=0.7, opacity=1.0),
    }

    for keyword, material in presets.items():
        if keyword in prompt:
            return material

    return MaterialProperties(name="default-concrete", color="#c7c9cc", roughness=0.85, opacity=1.0)


def build_object_name(shape: str, prompt: str) -> str:
    clean_prompt = re.sub(r"[^a-zA-Z0-9]+", "-", prompt.strip().lower()).strip("-")
    suffix = clean_prompt[:32] if clean_prompt else "generated"
    return f"{shape}-{suffix}"


def generate_cube(size: float) -> tuple[list[list[float]], list[list[int]]]:
    half = size / 2.0
    vertices = [
        [-half, -half, -half],
        [half, -half, -half],
        [half, half, -half],
        [-half, half, -half],
        [-half, -half, half],
        [half, -half, half],
        [half, half, half],
        [-half, half, half],
    ]
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [4, 6, 5],
        [4, 7, 6],
        [0, 4, 5],
        [0, 5, 1],
        [1, 5, 6],
        [1, 6, 2],
        [2, 6, 7],
        [2, 7, 3],
        [3, 7, 4],
        [3, 4, 0],
    ]
    return vertices, faces


def generate_cylinder(radius: float, height: float, segments: int) -> tuple[list[list[float]], list[list[int]]]:
    half_height = height / 2.0
    vertices: list[list[float]] = []
    faces: list[list[int]] = []

    for index in range(segments):
        angle = 2.0 * math.pi * index / segments
        x = round(radius * math.cos(angle), 6)
        y = round(radius * math.sin(angle), 6)
        vertices.append([x, y, -half_height])
        vertices.append([x, y, half_height])

    bottom_center_index = len(vertices)
    vertices.append([0.0, 0.0, -half_height])
    top_center_index = len(vertices)
    vertices.append([0.0, 0.0, half_height])

    for index in range(segments):
        next_index = (index + 1) % segments
        bottom_current = index * 2
        top_current = bottom_current + 1
        bottom_next = next_index * 2
        top_next = bottom_next + 1

        faces.append([bottom_current, bottom_next, top_current])
        faces.append([top_current, bottom_next, top_next])
        faces.append([bottom_center_index, bottom_next, bottom_current])
        faces.append([top_center_index, top_current, top_next])

    return vertices, faces
