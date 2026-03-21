from __future__ import annotations

import json
from pprint import pprint

from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    client = TestClient(app)
    prompts = [
        "cube size 6 red block",
        "blue cylinder height 12 radius 3",
    ]

    for prompt in prompts:
        response = client.post("/generate", json={"prompt": prompt})
        response.raise_for_status()
        body = response.json()
        print(f"Prompt: {prompt}")
        pprint(
            {
                "shape": body["shape"],
                "vertex_count": len(body["vertices"]),
                "face_count": len(body["faces"]),
                "material": body["material"],
                "dimensions": body["dimensions"],
            }
        )
        print("-" * 60)

    with open("sample_response.json", "w", encoding="utf-8") as handle:
        sample = client.post("/generate", json={"prompt": prompts[1]}).json()
        json.dump(sample, handle, indent=2)


if __name__ == "__main__":
    main()
