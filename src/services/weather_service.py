import httpx
from typing import Dict, Any, Optional

class WeatherService:
    """Service to interact with the Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"

    async def get_coordinates(self, city: str) -> Optional[Dict[str, float]]:
        """Get coordinates for a city name."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.GEO_URL,
                    params={"name": city, "count": 1, "language": "en", "format": "json"}
                )
                response.raise_for_status()
                data = response.json()
                if "results" in data and len(data["results"]) > 0:
                    result = data["results"][0]
                    return {
                        "latitude": result["latitude"],
                        "longitude": result["longitude"],
                        "name": result["name"],
                        "country": result.get("country", "")
                    }
                return None
            except httpx.HTTPError:
                return None

    async def get_current_weather(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """Get current weather for coordinates."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.BASE_URL,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current_weather": "true"
                    }
                )
                response.raise_for_status()
                return response.json().get("current_weather")
            except httpx.HTTPError:
                return None

    async def get_forecast(self, latitude: float, longitude: float, days: int = 3) -> Optional[Dict[str, Any]]:
        """Get weather forecast for coordinates."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.BASE_URL,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "daily": "temperature_2m_max,temperature_2m_min",
                        "forecast_days": days,
                        "timezone": "auto"
                    }
                )
                response.raise_for_status()
                return response.json().get("daily")
            except httpx.HTTPError:
                return None
