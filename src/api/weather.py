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

class ForecastDay(BaseModel):
    date: str
    max_temp: float
    min_temp: float

class ForecastResponse(BaseModel):
    city: str
    country: str
    forecast: list[ForecastDay]

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

@router.get("/forecast/{city}", response_model=ForecastResponse)
async def get_weather_forecast_for_city(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):
    """
    Get a 3-day weather forecast for a specific city.
    """
    # 1. Geocode the city
    location = await service.get_coordinates(city)
    if not location:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
        
    # 2. Get Forecast
    forecast_data = await service.get_forecast(location["latitude"], location["longitude"])
    if not forecast_data:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast data.")
    
    # 3. Format the response
    days = []
    for i in range(len(forecast_data["time"])):
        days.append(ForecastDay(
            date=forecast_data["time"][i],
            max_temp=forecast_data["temperature_2m_max"][i],
            min_temp=forecast_data["temperature_2m_min"][i]
        ))
        
    return ForecastResponse(
        city=location["name"],
        country=location["country"],
        forecast=days
    )
