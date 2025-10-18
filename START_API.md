# Starting the Mina API Server

This guide explains how to run the Mina Shopping Agent API server for frontend integration.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- All dependencies installed (see Installation section)

## Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Modern web framework for building APIs
- Uvicorn - ASGI server for running FastAPI
- WebSockets - For real-time communication
- Pydantic - Data validation
- All other Mina agent dependencies

## Running the Server

### Quick Start

Run the API server with default settings:

```bash
python api_server.py
```

The server will start on `http://0.0.0.0:8000` by default.

### Custom Configuration

You can configure the server using environment variables:

```bash
# Set custom host and port
export API_HOST=127.0.0.1
export API_PORT=8080

# Enable auto-reload for development
export API_RELOAD=true

python api_server.py
```

### Using Uvicorn Directly

For more control, you can run the server using uvicorn directly:

```bash
# Development mode with auto-reload
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

Once the server is running, you can access:

### 1. Root Endpoint
```
GET http://localhost:8000/
```
Returns API information and available endpoints.

### 2. Health Check
```
GET http://localhost:8000/api/health
```
Returns server status and integration availability.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "integrations": {
    "claude": true,
    "browser_use": false,
    "daytona": false
  }
}
```

### 3. Product Search
```
POST http://localhost:8000/api/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "category": "laptop",
  "budget_max": 3000,
  "priorities": ["Performance", "Battery Life"],
  "specific_needs": "For software development"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "product": {
        "name": "MacBook Pro 16\" M3 Max",
        "price": 3499.00,
        "retailer": "Apple Store",
        "url": "https://www.apple.com/...",
        "specs": {...},
        "reviews_summary": "Exceptional performance...",
        "rating": 4.8
      },
      "confidence_score": 92.5,
      "reasoning": "Based on comprehensive analysis...",
      "pros": ["Exceptional performance", "Outstanding battery life"],
      "cons": ["At the higher end of your budget"]
    }
  ],
  "total_products_analyzed": 3,
  "search_time_seconds": 2.45
}
```

### 4. WebSocket Connection
```
ws://localhost:8000/ws
```

Connect to the WebSocket endpoint for real-time search updates.

**Example messages:**

Start a search:
```json
{
  "type": "search",
  "requirements": {
    "category": "laptop",
    "budget_max": 3000,
    "priorities": ["Performance"]
  }
}
```

Receive progress updates:
```json
{
  "type": "progress",
  "status": "analyzing",
  "message": "Analyzing 3 products..."
}
```

Receive results:
```json
{
  "type": "results",
  "status": "completed",
  "recommendations": [...],
  "total_products_analyzed": 3
}
```

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

### Swagger UI
Visit `http://localhost:8000/docs` to access the Swagger UI where you can:
- View all available endpoints
- Test API endpoints directly in the browser
- See request/response schemas
- Try out the API with example data

### ReDoc
Visit `http://localhost:8000/redoc` for alternative documentation with a different interface.

## Testing the API

### Using cURL

**Health check:**
```bash
curl http://localhost:8000/api/health
```

**Product search:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "category": "laptop",
    "budget_max": 3000,
    "priorities": ["Performance", "Battery Life"],
    "specific_needs": ""
  }'
```

### Using Python Requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())

# Product search
search_data = {
    "category": "laptop",
    "budget_max": 3000,
    "priorities": ["Performance", "Battery Life"],
    "specific_needs": "For software development"
}

response = requests.post(
    "http://localhost:8000/api/search",
    json=search_data
)

results = response.json()
print(f"Found {results['total_products_analyzed']} products")
for rec in results['recommendations']:
    print(f"- {rec['product']['name']}: {rec['confidence_score']}% confidence")
```

### Using JavaScript Fetch

```javascript
// Health check
fetch('http://localhost:8000/api/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Product search
fetch('http://localhost:8000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    category: 'laptop',
    budget_max: 3000,
    priorities: ['Performance', 'Battery Life'],
    specific_needs: 'For software development'
  })
})
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.total_products_analyzed} products`);
    data.recommendations.forEach(rec => {
      console.log(`${rec.product.name}: ${rec.confidence_score}% confidence`);
    });
  });
```

## CORS Configuration

The API server is configured to accept requests from:
- `http://localhost:3000` (default Next.js development port)
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

If you need to add additional origins, edit the `allow_origins` list in `api_server.py`.

## Environment Variables

The API server supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | Server host address | `0.0.0.0` |
| `API_PORT` | Server port number | `8000` |
| `API_RELOAD` | Enable auto-reload (development) | `false` |
| `ANTHROPIC_API_KEY` | Claude API key | (optional) |
| `BROWSER_USE_API_KEY` | Browser Use API key | (optional) |
| `DAYTONA_API_KEY` | Daytona API key | (optional) |
| `GALILEO_API_KEY` | Galileo API key | (optional) |

Set these in your `.env` file or export them in your shell.

## Troubleshooting

### Port Already in Use

If you see an error that port 8000 is already in use:

```bash
# Use a different port
export API_PORT=8080
python api_server.py

# Or kill the process using the port
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Errors

If you see `ModuleNotFoundError` for fastapi or other dependencies:

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific packages
pip install fastapi uvicorn websockets
```

### CORS Errors

If the frontend can't connect due to CORS errors:

1. Check that the frontend is running on an allowed origin
2. Add your frontend URL to the `allow_origins` list in `api_server.py`
3. Restart the API server

### Performance Issues

For production deployment:

```bash
# Use multiple worker processes
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4

# Or use gunicorn with uvicorn workers
pip install gunicorn
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Integration with Frontend

The API is designed to work with the Next.js frontend. See the frontend repository for:

- API client implementation (`lib/api-client.ts`)
- React hooks (`hooks/useMinaSearch.ts`)
- Search interface components

## Next Steps

1. Start the API server: `python api_server.py`
2. Test the health endpoint: `curl http://localhost:8000/api/health`
3. Try the interactive docs: `http://localhost:8000/docs`
4. Connect your frontend application
5. Test end-to-end integration

## Production Deployment

For production deployment, consider:

1. **Use HTTPS**: Set up SSL/TLS certificates
2. **Environment variables**: Use proper secret management
3. **Process manager**: Use systemd, supervisor, or Docker
4. **Reverse proxy**: Use nginx or similar
5. **Monitoring**: Add logging and monitoring
6. **Rate limiting**: Add rate limiting middleware
7. **Authentication**: Add API key or OAuth authentication if needed

Example systemd service file:

```ini
[Unit]
Description=Mina API Server
After=network.target

[Service]
Type=simple
User=mina
WorkingDirectory=/opt/mina
Environment="PATH=/opt/mina/venv/bin"
ExecStart=/opt/mina/venv/bin/uvicorn api_server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/wildhash/Mina/issues)
- Check the main README.md for general documentation
- Review the API documentation at `/docs` endpoint
