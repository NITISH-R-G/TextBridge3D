```mermaid
graph TD
    User([User])

    subgraph Clients["Clients / Adapters"]
        revit["Revit Plugin"]
        sketchup["Sketchup Plugin"]
        solidworks["Solidworks Plugin"]
    end

    subgraph Services["Services"]
        app["App Service"]
    end

    User -->|Prompts| Clients
    revit -->|HTTP POST| app
    sketchup -->|HTTP POST| app
    solidworks -->|HTTP POST| app
```
