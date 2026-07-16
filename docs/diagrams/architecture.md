```mermaid
graph TD
    User([User])

    subgraph Clients["Clients / Adapters"]
        sketchup["Sketchup Plugin"]
        revit["Revit Plugin"]
        solidworks["Solidworks Plugin"]
    end

    subgraph Services["Services"]
        app["App Service"]
    end

    User -->|Prompts| Clients
    sketchup -->|HTTP POST| app
    revit -->|HTTP POST| app
    solidworks -->|HTTP POST| app
```
