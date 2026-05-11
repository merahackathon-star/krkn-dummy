from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.weather import router as weather_router

app = FastAPI(
    title="NexusWeather API",
    description="A Weather & Geolocation Wrapper API.",
    version="1.0.0",
)

# Allow CORS for local development and future web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(weather_router, prefix="/api/v1")

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint to ensure API is running."""
    return {"status": "ok", "service": "NexusWeather API"}
