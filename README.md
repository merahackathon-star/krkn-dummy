# NexusWeather API

A Weather & Geolocation Wrapper API built with FastAPI, designed for CI/CD, LLM documentation updates, and automated PR reviews.

## Getting Started

### 1. Conda Environment
This project uses Conda to manage dependencies (Python, Hugo, Go).

```bash
conda env create -f environment.yml
conda activate krkn
```

### 2. Running the API
The API is built using FastAPI.

```bash
uvicorn src.main:app --reload
```
View the Swagger UI documentation at `http://localhost:8000/docs`.

### 3. Running Tests
The project is set up with `pytest`, perfect for your `act` CI workflows.

```bash
python -m pytest tests/
```

### 4. Running the Documentation Site
The documentation is built with Hugo and the Docsy theme.

```bash
cd docs
hugo server
```
View the documentation at `http://localhost:1313`.

## CI/CD Pipeline & Automations

This project is fully equipped with CI/CD and automated review systems.

### 1. CodeRabbit (Automated PR Review)
We use CodeRabbit to automatically review Python code and Hugo Markdown documentation.
- **Setup:** Install the [CodeRabbit GitHub App](https://coderabbit.ai/) on your repository.
- **Config:** See `.coderabbit.yaml` for behavior rules.

### 2. Gemini Documentation Updater
A GitHub Action automatically queries the Gemini LLM when changes are pushed. It analyzes the `git diff` and opens a Draft PR updating the documentation in `docs/content/en/`.
- **Required Secrets:** You must add a `GEMINI_API_KEY` to your GitHub Repository Secrets.

### 3. Local Testing with `act`
You can test the GitHub Actions locally before pushing them!

**Installation (macOS):**
```bash
brew install act
```

**Setup Secrets:**
1. Copy the secrets template: `cp .secrets.example .secrets`
2. Add your actual `GEMINI_API_KEY` and a `GITHUB_TOKEN` to the `.secrets` file.

**Run the Pytest CI Workflow:**
```bash
act -j test -W .github/workflows/ci.yml
```

**Run the Gemini Updater Workflow:**
```bash
act -j update-docs --secret-file .secrets -W .github/workflows/gemini_docs_updater.yml
```
