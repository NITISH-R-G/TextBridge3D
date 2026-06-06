import os
import json
import re

def analyze_repo(root_dir="."):
    graph = {
        "frameworks": [],
        "languages": [],
        "dependencies": {
            "python": [],
            "csharp": [],
            "ruby": []
        },
        "services": [],
        "clients": [],
        "directories": {}
    }

    def add_unique(key, value):
        if value not in graph[key]:
            graph[key].append(value)

    def add_dep(lang, dep):
        if dep not in graph["dependencies"][lang]:
            graph["dependencies"][lang].append(dep)

    for root, dirs, files in os.walk(root_dir):
        if ".git" in root or ".venv" in root or "docs" in root:
            continue

        rel_path = os.path.relpath(root, root_dir)
        if rel_path == ".":
            rel_path = "/"

        graph["directories"][rel_path] = files

        # Detect services based on directory name
        if rel_path == "app":
            if "main.py" in files:
                add_unique("services", "app")

        # Detect clients
        if rel_path.startswith("clients/"):
            parts = rel_path.split("/")
            if len(parts) >= 2:
                add_unique("clients", parts[1])

        for file in files:
            file_path = os.path.join(root, file)

            # Identify Python
            if file.endswith(".py"):
                add_unique("languages", "Python")
            # Identify Ruby
            elif file.endswith(".rb"):
                add_unique("languages", "Ruby")
            # Identify C#
            elif file.endswith(".cs"):
                add_unique("languages", "C#")

            # Parse requirements.txt
            if file == "requirements.txt":
                try:
                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                dep_name = re.split(r'[=<>~]', line)[0]
                                add_dep("python", dep_name)
                                if dep_name == "fastapi":
                                    add_unique("frameworks", "FastAPI")
                                elif dep_name == "pydantic":
                                    add_unique("frameworks", "Pydantic")
                except Exception as e:
                    pass

            # Parse .csproj
            elif file.endswith(".csproj"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        refs = re.findall(r'<Reference Include="([^"]+)"', content)
                        for ref in refs:
                            ref_name = ref.split(',')[0]
                            add_dep("csharp", ref_name)
                except Exception as e:
                    pass

    with open("repo_knowledge_graph.json", "w") as f:
        json.dump(graph, f, indent=2)

if __name__ == "__main__":
    analyze_repo()
