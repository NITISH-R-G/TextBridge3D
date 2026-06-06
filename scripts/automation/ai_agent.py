import argparse
import os
import json
import subprocess

def run_heuristic_review(changed_files):
    """Fallback review logic if no API key is present."""
    print("--- Using Heuristic Repository Analyzer ---")
    arch_changes = []

    for file in changed_files:
        if "requirements.txt" in file:
            arch_changes.append(f"[DEP] Backend dependencies modified in {file}.")
        if ".csproj" in file:
            arch_changes.append(f"[BUILD] C# project {file} modified.")
        if ".rb" in file:
            arch_changes.append(f"[CLIENT] Ruby SketchUp client modified: {file}")
        if file.endswith(".py") and "app/" in file:
            arch_changes.append(f"[API/LOGIC] Backend layer modified: {file}.")

    if not arch_changes:
        print("No major architectural modifications detected via heuristics.")
    else:
        for change in arch_changes:
            print(change)
    print("Recommendation: Trigger auto-documentation via main branch push.")

def run_llm_review(changed_files, diff_content, api_key):
    """Real AI review logic if OPENAI_API_KEY is present."""
    print("--- Using AI LLM Analyzer ---")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"Review the following changes for architectural impact and suggest documentation updates:\n\nFiles Changed:\n{', '.join(changed_files)}\n\nDiff Content:\n{diff_content}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior AI repository maintainer. Analyze diffs to detect structural changes and output clear documentation suggestions."},
                {"role": "user", "content": prompt}
            ]
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Failed to use LLM due to: {e}. Falling back to heuristics.")
        run_heuristic_review(changed_files)

def review_changes(diff_file):
    print("=== AI PR Reviewer Started ===")

    if not os.path.exists(diff_file):
        print("No diff file found.")
        return

    with open(diff_file, "r") as f:
        changed_files = f.read().splitlines()

    if not changed_files:
        print("No changed files to review.")
        return

    print("Changed Files:")
    for file in changed_files:
        print(f" - {file}")

    # Extract git diff context to pass to the LLM (if available)
    try:
        diff_content = subprocess.check_output(["git", "diff", "HEAD"], text=True)
    except Exception:
        diff_content = "(Diff content not available)"

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        run_llm_review(changed_files, diff_content, api_key)
    else:
        print("\nNote: OPENAI_API_KEY not found in environment.")
        run_heuristic_review(changed_files)

    print("=== Review Complete ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI PR Review Agent")
    parser.add_argument("--diff-file", type=str, help="Path to file containing list of changed files")
    args = parser.parse_args()

    if args.diff_file:
        review_changes(args.diff_file)
    else:
        print("Please provide a --diff-file argument.")
