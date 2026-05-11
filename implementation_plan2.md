# Goal Description

The goal is to build a comprehensive end-to-end CI/CD pipeline for the NexusWeather API. This pipeline will automatically test the code, use the Gemini API to intelligently update your Hugo documentation by analyzing code changes, automatically open Draft PRs with those documentation updates, and integrate CodeRabbit for automated PR and documentation reviews. We will also set up `act` so you can test these workflows locally before pushing to GitHub.

## User Review Required

> [!IMPORTANT]
> 1. **Gemini API Key:** The automated documentation script will require a `GEMINI_API_KEY`. When testing locally with `act`, you will need to provide this in a local `.secrets` file. When deploying to GitHub, you will need to add it as a Repository Secret.
> 2. **GitHub Token:** The workflow uses `GITHUB_TOKEN` to create the Draft PR. `act` can sometimes be finicky with standard tokens. For local testing with `act` that involves creating PRs, you may need a Personal Access Token (PAT).
> 3. **CodeRabbit Installation:** I can create the configuration file (`.coderabbit.yaml`), but you will need to manually install the CodeRabbit app on your GitHub repository for it to function.
> 
> Please confirm if you are comfortable managing these secrets and installing the CodeRabbit GitHub App.

## Proposed Changes

We will introduce the following files to support the CI/CD and automation infrastructure:

### 1. GitHub Actions Workflows (`.github/workflows/`)

#### [NEW] `ci.yml`
- **Purpose:** Standard Continuous Integration.
- **Triggers:** On `push` and `pull_request` to the `main` branch.
- **Steps:** Sets up Python, installs dependencies from `environment.yml`, and runs `pytest`.

#### [NEW] `gemini_docs_updater.yml`
- **Purpose:** Automates documentation updates using Gemini and creates Draft PRs.
- **Triggers:** On `push` to the `main` branch (when a feature is merged) OR manually triggered via `workflow_dispatch`.
- **Steps:**
    1. Checks out the repository.
    2. Runs a custom Python script that fetches the recent `git diff`.
    3. The script sends the diff to the **Gemini API**, asking it to update the Hugo Markdown files in `docs/content/en/`.
    4. Uses the `peter-evans/create-pull-request` action to automatically bundle those changes into a new Draft Pull Request.

### 2. CodeRabbit Configuration

#### [NEW] `.coderabbit.yaml`
- **Purpose:** Configures CodeRabbit's behavior to review both Python code and Markdown documentation.
- **Settings:** We will configure it to provide high-level summaries, focus on the FastAPI logic, and review the tone and accuracy of the Hugo documentation.

### 3. Gemini Automation Script

#### [NEW] `scripts/update_docs.py`
- **Purpose:** The bridge between your code and the Gemini API.
- **Logic:**
    - Uses `google-generativeai` to interface with Gemini.
    - Reads the latest `git diff`.
    - Prompts Gemini: *"Given these code changes, how should the API documentation in `docs/content/en/api.md` be updated?"*
    - Automatically overwrites the targeted markdown files with Gemini's suggested changes.

#### [MODIFY] `environment.yml`
- Add `google-generativeai` and `gitpython` to the dependencies to support the new script.

### 4. Local Testing with `act` Preparation

#### [NEW] `.secrets.example`
- A template file to show you how to securely pass your `GEMINI_API_KEY` to `act` when running workflows locally.

## Verification Plan

### Manual Verification via `act`
1.  **Install `act`:** We will verify that you have `act` installed (e.g., via Homebrew `brew install act`).
2.  **Test CI Locally:** We will run `act -j test -W .github/workflows/ci.yml` locally to ensure the test suite runs correctly inside a simulated GitHub Actions runner.
3.  **Test Gemini Updater Locally:**
    - I will guide you to place a mock or real `GEMINI_API_KEY` in a `.secrets` file.
    - We will make a dummy change to `src/api/weather.py`.
    - We will run `act -j update-docs --secret-file .secrets -W .github/workflows/gemini_docs_updater.yml`.
    - We will verify that the script successfully queries Gemini and modifies the local `docs/content/en/api.md` file (Note: the `create-pull-request` step usually skips PR creation when run locally in `act`, but the file modifications will be visible).
