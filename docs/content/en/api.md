---
title: API Reference
description: "Reference for NexusWeather API endpoints."
weight: 10
---

## Endpoints

### `GET /api/v1/weather/current/{city}`

Fetches current weather for a specified city.

**Parameters:**
- `city` (string): The name of the city.

**Response:**
```json
{
  "city": "London",
  "country": "United Kingdom",
  "temperature": 15.0,
  "windspeed": 10.0,
  "winddirection": 180.0
}
```

### `GET /api/v1/weather/forecast/{city}`

Fetches a 3-day weather forecast for a specified city.

**Parameters:**
- `city` (string): The name of the city.

**Response:**
```json
{
  "city": "London",
  "country": "United Kingdom",
  "forecast": [
    {
      "date": "2023-10-27",
      "max_temp": 15.5,
      "min_temp": 10.2
    },
    {
      "date": "2023-10-28",
      "max_temp": 16.0,
      "min_temp": 11.0
    },
    {
      "date": "2023-10-29",
      "max_temp": 14.5,
      "min_temp": 9.5
    }
  ]
}
