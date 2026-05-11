from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

# Dependency injection for the service
def get_weather_service():
    return WeatherService()

class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    windspeed: float
    winddirection: float

@router.get("/current/{city}", response_model=WeatherResponse)
async def get_current_weather_for_city(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):
    """
    Get the current weather for a specific city.
    Uses Open-Meteo for Geocoding and Weather data.
    """
    # 1. Geocode the city
    location = await service.get_coordinates(city)
    if not location:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
        
    # 2. Get Weather
    weather = await service.get_current_weather(location["latitude"], location["longitude"])
    if not weather:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data.")
        
    return WeatherResponse(
        city=location["name"],
        country=location["country"],
        temperature=weather["temperature"],
        windspeed=weather["windspeed"],
        winddirection=weather["winddirection"]
    )
