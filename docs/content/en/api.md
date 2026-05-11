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
