import json
import os

def generate_diagrams():
    with open("repo_knowledge_graph.json", "r") as f:
        graph = json.load(f)

    os.makedirs("docs/diagrams", exist_ok=True)

    # 1. Dynamic Component Architecture Diagram
    arch_diagram = """```mermaid
graph TD
    User([User])

    subgraph Clients["Clients / Adapters"]
"""
    for client in graph["clients"]:
        arch_diagram += f'        {client}["{client.capitalize()} Plugin"]\n'

    arch_diagram += """    end

    subgraph Services["Services"]
"""
    for service in graph["services"]:
        arch_diagram += f'        {service}["{service.capitalize()} Service"]\n'

    arch_diagram += """    end

    User -->|Prompts| Clients
"""
    for client in graph["clients"]:
        for service in graph["services"]:
            arch_diagram += f'    {client} -->|HTTP POST| {service}\n'

    arch_diagram += "```\n"

    with open("docs/diagrams/architecture.md", "w") as f:
        f.write(arch_diagram)


    # 2. Dynamic Tech Stack Diagram
    stack_diagram = """```mermaid
mindmap
  root((Project))
    Backend
      Python
"""
    for py_dep in graph["dependencies"]["python"]:
        stack_diagram += f"        {py_dep}\n"

    stack_diagram += """    Clients
      C#
"""
    for cs_dep in graph["dependencies"]["csharp"]:
        stack_diagram += f"        {cs_dep}\n"

    stack_diagram += """      Ruby
        SketchUp API
```\n"""

    with open("docs/diagrams/tech_stack.md", "w") as f:
        f.write(stack_diagram)

if __name__ == "__main__":
    generate_diagrams()
