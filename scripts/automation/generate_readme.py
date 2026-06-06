import json
import os
import re

def build_readme():
    with open("repo_knowledge_graph.json", "r") as f:
        graph = json.load(f)

    # Load architecture diagram
    arch_diagram = ""
    if os.path.exists("docs/diagrams/architecture.md"):
        with open("docs/diagrams/architecture.md", "r") as f:
            arch_diagram = f.read()

    tech_stack_diagram = ""
    if os.path.exists("docs/diagrams/tech_stack.md"):
        with open("docs/diagrams/tech_stack.md", "r") as f:
            tech_stack_diagram = f.read()

    # Create directory structure string
    dir_struct = "```text\n"
    for directory, files in graph["directories"].items():
        if directory == "/":
            for file in files:
                dir_struct += f"{file}\n"
        else:
            dir_struct += f"{directory}/\n"
            for file in files:
                dir_struct += f"  {file}\n"
    dir_struct += "```\n"

    dynamic_content = f"""
<!-- AUTO-GENERATED-START -->
## System Architecture
{arch_diagram}

## Technology Stack
{tech_stack_diagram}

### Identified Languages and Frameworks
- **Languages**: {', '.join(graph['languages'])}
- **Frameworks**: {', '.join(graph['frameworks'])}

## Generated Repository Structure
{dir_struct}
<!-- AUTO-GENERATED-END -->
"""

    with open("README.md", "r") as f:
        readme_content = f.read()

    # If the tags exist, replace everything between them
    if "<!-- AUTO-GENERATED-START -->" in readme_content and "<!-- AUTO-GENERATED-END -->" in readme_content:
        new_content = re.sub(
            r'<!-- AUTO-GENERATED-START -->.*?<!-- AUTO-GENERATED-END -->',
            dynamic_content.strip(),
            readme_content,
            flags=re.DOTALL
        )
    else:
        # Otherwise, append the block to the end of the README
        new_content = readme_content + "\n" + dynamic_content.strip() + "\n"

    with open("README.md", "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    build_readme()
