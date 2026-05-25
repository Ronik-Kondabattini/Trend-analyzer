# TrendPulse API Documentation

This document provides details about the API endpoints available in the Trend Analyzer backend.

## Authentication
Currently, the API endpoints use session-based authentication provided by Django. For API testing, you must be logged in via the Django frontend or pass the appropriate `CSRF` and `Session` cookies.

## Endpoints

### 1. Analyze Topic
- **Endpoint:** `/api/analyze/`
- **Method:** `POST`
- **Description:** Submits a topic for trend analysis and generates YouTube suggestions and content ideas.

#### Request Example (JSON)
```json
{
  "topic": "Artificial Intelligence in 2026"
}
```

#### Response Example
```json
{
  "status": "success",
  "data": {
    "trend_score": 92,
    "metrics": {
      "search_volume": "High",
      "growth_rate": "+15%"
    },
    "suggestions": [
      {"title": "AI in 2026: What to Expect", "type": "Video"}
    ],
    "ideas": [
      "Top 5 AI tools you must use this year"
    ]
  }
}
```

### 2. Search History
- **Endpoint:** `/api/history/`
- **Method:** `GET`
- **Description:** Retrieves the user's past search queries and analysis results.

### 3. Saved Ideas
- **Endpoint:** `/api/saved-ideas/`
- **Method:** `GET`
- **Description:** Retrieves the content ideas the user has saved to their profile.
