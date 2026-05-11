from fastapi.testclient import TestClient
from src.main import app
from src.api.weather import get_weather_service
import pytest

client = TestClient(app)

class MockWeatherService:
    async def get_coordinates(self, city: str):
        if city.lower() == "london":
            return {"latitude": 51.5085, "longitude": -0.1257, "name": "London", "country": "United Kingdom"}
        return None

    async def get_current_weather(self, latitude: float, longitude: float):
        if latitude == 51.5085:
            return {"temperature": 15.0, "windspeed": 10.0, "winddirection": 180.0}
        return None

app.dependency_overrides[get_weather_service] = MockWeatherService

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "NexusWeather API"}

def test_get_weather_success():
    response = client.get("/api/v1/weather/current/london")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "London"
    assert data["country"] == "United Kingdom"
    assert data["temperature"] == 15.0

def test_get_weather_not_found():
    response = client.get("/api/v1/weather/current/unknowncity")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
