# Native Client Samples

These client samples all call the same local FastAPI server at `http://127.0.0.1:8000/generate`.

## Revit 2023

Project: `clients/revit/TextToModeling.Revit`

- .NET Framework 4.8 WPF class library
- Implements `IExternalCommand`
- Opens a prompt window
- Calls the backend
- Converts returned vertices and faces into a `DirectShape` using `TessellatedShapeBuilder`

To use it, build the DLL and update `TextToModeling.addin` with the actual assembly path.

## SketchUp

Folder: `clients/sketchup`

- Ruby extension loader plus `UI::HtmlDialog`
- Sends the prompt with `net/http`
- Parses the JSON response
- Draws it with `Geom::PolygonMesh` and `entities.add_faces_from_mesh`

Package it as an `.rbz` with the loader file and the `text_to_modeling` folder.

## SolidWorks

Project: `clients/solidworks/TextToModeling.SolidWorks`

- .NET Framework 4.8 Windows Forms add-in
- Creates a Taskpane control
- Sends the prompt to the backend
- Receives the mesh response
- Shows where to hand off into a real feature-generation pipeline

The SolidWorks sample is intentionally conservative: it wires up the taskpane and API call, then leaves the final geometry strategy as a host-specific next step because `InsertFeature` alone is too generic for arbitrary mesh reconstruction.
