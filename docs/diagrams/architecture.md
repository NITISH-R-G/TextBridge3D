```mermaid
graph TD
    User([User])

    subgraph Clients["Clients / Adapters"]
        solidworks["Solidworks Plugin"]
        sketchup["Sketchup Plugin"]
        revit["Revit Plugin"]
    end

    subgraph Services["Services"]
        app["App Service"]
    end

    User -->|Prompts| Clients
    solidworks -->|HTTP POST| app
    sketchup -->|HTTP POST| app
    revit -->|HTTP POST| app
```
