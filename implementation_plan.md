# Goal Description

The goal is to create the **NexusWeather API**, a Weather & Geolocation Wrapper API, alongside a documentation site powered by the Hugo static site generator using the Docsy theme. The documentation will reside in a `/docs` folder. The entire project will be developed within a newly created Conda environment named `krkn`.

The project is designed to act as a strong foundation for a future CI/CD pipeline (using `act`), automated LLM documentation updates (via Gemini), and automated PR reviews (via CodeRabbit). 

## User Review Required

> [!IMPORTANT]
> The Docsy theme requires the **Hugo Extended** version and **Go** (for Hugo Modules). 
> I will configure the Conda environment to automatically install `hugo`, `go`, and `python` all together to keep everything clean and encapsulated.
> 
> For the NexusWeather API, I will use **FastAPI**, as it's the modern standard for building Python APIs, naturally generates OpenAPI schemas, and is highly testable (perfect for your future CI/CD goals). 
> Please let me know if this plan looks good to you so I can begin execution!

## Open Questions

> [!NOTE]
> 1. Since we are building a wrapper API, do you want me to mock the external weather/geolocation data for now, or would you prefer I integrate with a free public API (like Open-Meteo) right away? (I will default to integrating with Open-Meteo since it requires no API keys and is great for testing).

## Proposed Changes

We will create the following robust project structure:
```text
krkn-dummy/
├── .github/              # (Future) Prepared for CI/CD workflows and CodeRabbit
├── src/                  # NexusWeather API source code
│   ├── api/              # API routing and endpoints
│   ├── core/             # Configuration and utilities
│   ├── services/         # External API wrapper logic (Weather/Geolocation)
│   └── main.py           # FastAPI application entry point
├── tests/                # Prepared for pytest (for future CI/CD with 'act')
├── docs/                 # Hugo documentation site
│   ├── hugo.toml         # Hugo configuration using Docsy
│   ├── content/          # Markdown documentation files (Target for future LLM updates)
│   └── ...
├── environment.yml       # Conda environment definition (includes FastAPI, Uvicorn, Pytest)
└── README.md             # Top-level instructions
```

### 1. Conda Environment Setup
- Create an `environment.yml` defining the `krkn` environment.
- The environment will include `python`, `hugo`, `go`, `fastapi`, `uvicorn`, `httpx` (for making external requests), and `pytest` (for your future CI).
- Execute `conda env create -f environment.yml`.

### 2. NexusWeather Application (FastAPI)
- Scaffold a clean, modular FastAPI application in the `src/` directory.
- Create a basic `/weather` endpoint that wraps a public weather service (e.g., Open-Meteo).
- Include basic `tests/` to ensure your future `act` CI/CD pipeline has something to run.

### 3. Hugo and Docsy Setup
- Initialize a new Hugo site in the `docs` directory using `hugo new site docs`.
- Initialize a Go module (`go mod init github.com/yourusername/nexusweather-docs`).
- Configure Hugo to use the Docsy theme via Hugo Modules by editing `hugo.toml`.
- Create an initial `_index.md` and basic documentation structure that your future Gemini LLM workflow can easily target and update.

### 4. Integration and Scripts
- Provide instructions in `README.md` on activating the Conda environment, running the FastAPI server locally, serving the documentation, and running tests.

## Verification Plan

### Automated Tests
- We will write a basic Pytest suite in `tests/` and run it to verify the API logic works locally. This prepares you for your `act` CI pipeline.

### Manual Verification
1.  **Conda**: Verify the environment is created successfully (`conda activate krkn`).
2.  **FastAPI**: Run `uvicorn src.main:app --reload` and verify the API responds at `http://localhost:8000/docs` (Swagger UI).
3.  **Documentation**: Run `cd docs && hugo server` and verify the Docsy site renders at `http://localhost:1313`.
