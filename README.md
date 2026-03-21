# TextBridge3D

TextBridge3D is a cross-platform text-to-modeling prototype for design software. It uses one shared FastAPI backend to convert a text prompt into simple 3D geometry, then connects that geometry into native client adapters for Revit, SketchUp, and SolidWorks.

The current version is intentionally narrow and stable:

- The backend supports `cube` and `cylinder`.
- Geometry is generated deterministically from prompt keywords.
- Revit and SketchUp consume mesh-style geometry with `vertices` and `faces`.
- SolidWorks consumes the shared response and reconstructs simple primitive features from returned dimensions.

## Repository Structure

```text
app/
  __init__.py
  main.py
  schemas.py
  generators.py
clients/
  README.md
  revit/
  sketchup/
  solidworks/
examples/
  cube-request.json
  cylinder-request.json
scripts/
  smoke_test.py
requirements.txt
README.md
```

## Architecture Overview

TextBridge3D is designed around one shared contract and several thin host adapters.

### Shared Backend

The FastAPI backend accepts a prompt and returns a normalized geometry payload:

- `shape`
- `dimensions`
- `vertices`
- `faces`
- `material`
- `meta`

This shared contract keeps the modeling logic in one place and reduces drift between hosts.

### Native Adapters

Each client plugin is intentionally thin:

- `Revit`: WPF window -> HTTP POST -> `DirectShape` via `TessellatedShapeBuilder`
- `SketchUp`: `UI::HtmlDialog` -> HTTP POST -> `Geom::PolygonMesh` and `add_faces_from_mesh`
- `SolidWorks`: Taskpane -> HTTP POST -> primitive reconstruction into an extrusion

This is the practical way to make the product interchangeable across very different CAD platforms. It is not one binary plugin, but one shared product architecture with native host implementations.

## Features

- Text prompt input through a simple API
- Rule-based shape detection
- Deterministic cube and cylinder generation
- Mesh response with vertices and triangle faces
- Basic material metadata
- Revit 2023 adapter sample
- SketchUp extension sample
- SolidWorks add-in sample

## Backend Installation Guide

### Requirements

- Python `3.12+`
- `pip`

Python `3.14` can work, but dependency compatibility may depend on current wheel availability for `pydantic-core`.

### Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Run the Server

```powershell
python -m uvicorn app.main:app --reload
```

The server will start at:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Health Check

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

## API Guide

### Endpoint

`POST /generate`

### Request Body

```json
{
  "prompt": "blue cylinder height 12 radius 3"
}
```

### Response Shape

```json
{
  "shape": "cylinder",
  "dimensions": {
    "height": 12,
    "radius": 3,
    "segments": 16
  },
  "vertices": [[0, 0, 0]],
  "faces": [[0, 1, 2]],
  "material": {
    "name": "matte-blue",
    "color": "#3d7be0",
    "roughness": 0.7,
    "opacity": 1.0
  },
  "meta": {
    "original_prompt": "blue cylinder height 12 radius 3",
    "object_name": "cylinder-blue-cylinder-height-12-rad",
    "generator": "rule-based-text-to-3d-demo"
  }
}
```

### Example Requests

See:

- [cube-request.json](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\examples\cube-request.json)
- [cylinder-request.json](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\examples\cylinder-request.json)

Example PowerShell call:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/generate `
  -ContentType "application/json" `
  -Body (Get-Content .\examples\cylinder-request.json -Raw)
```

## Prompt Rules

The current generator is rule-based. It inspects prompt text for keywords and optional numeric values.

### Supported Shape Keywords

- `cube`
- `box`
- `block`
- `square`
- `cylinder`
- `tube`
- `column`
- `round`
- `pipe`

### Supported Dimension Keywords

- `size`
- `height`
- `radius`
- `segments`

### Supported Material Keywords

- `glass`
- `metal`
- `wood`
- `red`
- `blue`
- `green`

If no supported shape is detected, the backend defaults to a cube.

## Smoke Testing

Run the in-process smoke test after dependencies are installed:

```powershell
python scripts\smoke_test.py
```

This script:

- sends a cube prompt
- sends a cylinder prompt
- prints summary information
- writes a sample response to `sample_response.json`

## Revit 2023 Installation Guide

Project path:

- [TextToModeling.Revit.csproj](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\revit\TextToModeling.Revit\TextToModeling.Revit.csproj)

### Requirements

- Autodesk Revit 2023
- Visual Studio 2022 or similar .NET Framework IDE
- .NET Framework `4.8`

### Setup

1. Open the Revit project in Visual Studio.
2. Verify reference hint paths:
   - `C:\Program Files\Autodesk\Revit 2023\RevitAPI.dll`
   - `C:\Program Files\Autodesk\Revit 2023\RevitAPIUI.dll`
3. Build the project in `Release`.
4. Update the assembly path inside:
   - [TextToModeling.addin](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\revit\TextToModeling.Revit\TextToModeling.addin)
5. Copy the `.addin` file into:
   - `%AppData%\Autodesk\Revit\Addins\2023\`

### Main Revit Files

- [GenerateMeshCommand.cs](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\revit\TextToModeling.Revit\GenerateMeshCommand.cs)
- [PromptWindow.xaml](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\revit\TextToModeling.Revit\PromptWindow.xaml)
- [PromptWindow.xaml.cs](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\revit\TextToModeling.Revit\PromptWindow.xaml.cs)
- [RevitMeshBuilder.cs](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\revit\TextToModeling.Revit\RevitMeshBuilder.cs)

### Revit Test Flow

1. Start the FastAPI backend.
2. Launch Revit.
3. Run the add-in command.
4. Enter a prompt such as `red cube size 6`.
5. Confirm a `DirectShape` appears in the active document.

## SketchUp Installation Guide

### Requirements

- SketchUp with Ruby extension support

### Files

- [text_to_modeling.rb](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\sketchup\text_to_modeling.rb)
- [main.rb](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\sketchup\text_to_modeling\main.rb)

### Install As `.rbz`

1. Zip these two items together:
   - `text_to_modeling.rb`
   - `text_to_modeling/`
2. Rename the zip file to `.rbz`.
3. In SketchUp, open `Extension Manager`.
4. Choose `Install Extension...`
5. Select the `.rbz`.

### Manual Install

Copy the loader file and folder into SketchUp's `Plugins` directory.

### SketchUp Test Flow

1. Start the FastAPI backend.
2. Open SketchUp.
3. Launch `Text To Modeling` from the menu.
4. Enter a prompt such as `blue cylinder height 12 radius 3`.
5. Confirm the generated geometry appears in the active model.

## SolidWorks Installation Guide

Project path:

- [TextToModeling.SolidWorks.csproj](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\solidworks\TextToModeling.SolidWorks\TextToModeling.SolidWorks.csproj)

### Requirements

- SolidWorks
- Visual Studio
- SolidWorks interop assemblies
- .NET Framework `4.8`

### Setup

1. Open the project in Visual Studio.
2. Add or verify references:
   - `SolidWorks.Interop.sldworks`
   - `SolidWorks.Interop.swconst`
3. Build the project.
4. Register the assembly for COM if your environment does not do it automatically.
5. Load the add-in in SolidWorks.

### Main SolidWorks Files

- [SolidWorksAddIn.cs](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\solidworks\TextToModeling.SolidWorks\SolidWorksAddIn.cs)
- [TaskpaneControl.cs](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\solidworks\TextToModeling.SolidWorks\TaskpaneControl.cs)
- [FastApiClient.cs](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\solidworks\TextToModeling.SolidWorks\FastApiClient.cs)

### SolidWorks Test Flow

1. Start the FastAPI backend.
2. Open a part document.
3. Open the taskpane.
4. Submit a prompt such as `red cube size 6`.
5. Confirm an extruded feature is created.

### SolidWorks Note

The current SolidWorks sample is primitive-oriented. It uses the shared response and reconstructs a cube or cylinder extrusion from dimensions rather than rebuilding a full triangle mesh body.

## Skills Used

The work in this repository was developed using a design-first workflow and then implemented in code.

Skills used during the process:

- `brainstorming`
  Used to define the architecture before implementation. This was important because the original goal covered multiple host applications and one shared backend.
- Native code implementation workflow
  Used to create the FastAPI backend and the three host adapters in a way that preserves a shared API contract.

## Development Notes

- The backend is intentionally simple and deterministic.
- The shared response contract is the most important part of the repository.
- Revit and SketchUp are currently the best targets for validating full mesh-based generation.
- SolidWorks is included as a practical host adapter sample for primitive reconstruction.

## Limitations

- This is not a production text-to-3D system.
- The backend is rule-based, not ML-based.
- Only `cube` and `cylinder` are supported.
- The generated geometry is simple and intended for plugin integration testing.
- Host-specific build and runtime verification depends on local installation of Revit, SketchUp, and SolidWorks.

## Recommended Next Steps

- Add backend unit tests for prompt parsing and mesh generation
- Add API versioning
- Add more primitives such as `cone`, `sphere`, and `extrusion`
- Add better material mapping
- Add logging and error envelopes
- Add packaging scripts for Revit, SketchUp, and SolidWorks releases

## References

- [clients/README.md](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\clients\README.md)
- [app/main.py](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\app\main.py)
- [app/generators.py](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\app\generators.py)
- [app/schemas.py](C:\Users\nitis\OneDrive\Documents\Architecture Neon task\app\schemas.py)
