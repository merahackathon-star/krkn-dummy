import os
import sys
import google.generativeai as genai
from git import Repo

def get_git_diff():
    try:
        repo = Repo(os.getcwd())
        # Getting diff against HEAD~1 (assuming script runs after a commit)
        # For a PR, you might want to diff against main.
        # This simple version diffs the working tree against HEAD if there are uncommitted changes,
        # or HEAD~1 if it's running in CI after a commit.
        if repo.is_dirty():
            return repo.git.diff("HEAD")
        else:
            return repo.git.diff("HEAD~1")
    except Exception as e:
        print(f"Error getting git diff: {e}")
        return ""

def update_documentation():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    genai.configure(api_key=api_key)
    
    # Read current documentation
    doc_path = "docs/content/en/api.md"
    try:
        with open(doc_path, "r") as f:
            current_docs = f.read()
    except FileNotFoundError:
        print(f"Documentation file not found at {doc_path}")
        sys.exit(1)

    git_diff = get_git_diff()
    if not git_diff:
        print("No code changes detected to document.")
        sys.exit(0)

    print("Analyzing code changes with Gemini...")

    prompt = f"""
    You are a technical writer maintaining a Hugo Docsy site.
    Below is the current API documentation markdown file:
    
    ```markdown
    {current_docs}
    ```
    
    Below is the recent Git Diff of the code:
    
    ```diff
    {git_diff}
    ```
    
    Task: Update the API documentation to reflect any changes introduced in the diff.
    - If there are new endpoints, add them.
    - If existing endpoints changed (parameters, return types), update them.
    - Only output the raw, updated markdown content. Do not include markdown codeblock fences (```markdown) around the entire output.
    - Preserve the Hugo front matter (e.g. --- title: API Reference ---).
    - If the git diff does not require documentation updates, return the original markdown unchanged.
    """

    try:
        # Using gemini-1.5-pro for complex coding/doc tasks
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        new_docs = response.text.strip()
        
        # Quick cleanup in case the LLM wrapped it in markdown tags
        if new_docs.startswith("```markdown"):
            new_docs = new_docs[11:]
        if new_docs.startswith("```"):
            new_docs = new_docs[3:]
        if new_docs.endswith("```"):
            new_docs = new_docs[:-3]
            
        new_docs = new_docs.strip()

        if new_docs != current_docs.strip():
            with open(doc_path, "w") as f:
                f.write(new_docs + "\n")
            print("Documentation successfully updated.")
        else:
            print("No documentation updates required.")

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_documentation()
