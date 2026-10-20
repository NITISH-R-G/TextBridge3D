```mermaid
graph TD
    User([User])

    subgraph Clients["Clients / Adapters"]
        sketchup["Sketchup Plugin"]
        solidworks["Solidworks Plugin"]
        revit["Revit Plugin"]
    end

    subgraph Services["Services"]
        app["App Service"]
    end

    User -->|Prompts| Clients
    sketchup -->|HTTP POST| app
    solidworks -->|HTTP POST| app
    revit -->|HTTP POST| app
```
