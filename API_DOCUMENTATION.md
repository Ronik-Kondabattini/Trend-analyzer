# API Documentation

## Overview
This document provides detailed information about the API endpoints available for the Trend Analyzer project.

## Authentication
All API requests require authentication using an API token. Include the token in the header as follows:

```http
Authorization: Bearer YOUR_API_TOKEN
```

## Endpoints

### 1. Get Trends
- **Endpoint:** `/api/trends`
- **Method:** `GET`

#### Request Example
```http
GET /api/trends HTTP/1.1
Host: example.com
Authorization: Bearer YOUR_API_TOKEN
```

#### Response Example
```json
{
  "trends": [
    {
      "id": 1,
      "name": "Trending Topic",
      "score": 75
    }
  ]
}
```

### 2. Create Trend
- **Endpoint:** `/api/trends`
- **Method:** `POST`

#### Request Example
```http
POST /api/trends HTTP/1.1
Host: example.com
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json

{
  "name": "New Trend",
  "category": "Technology"
}
```

#### Response Example
```json
{
  "message": "Trend created successfully",
  "trendId": 2
}
```

### Error Handling
Common error responses include:
- **401 Unauthorized**: Invalid or missing token.
- **404 Not Found**: The requested resource does not exist.

### Code Samples

#### Python Example
```python
import requests

url = 'https://example.com/api/trends'
headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f'Error: {response.status_code}')
```

#### JavaScript Example
```javascript
fetch('https://example.com/api/trends', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer YOUR_API_TOKEN'
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```