# Frontend Integration Guide

This guide explains how to integrate the Mina Shopping Agent API with a frontend application (Next.js, React, or any JavaScript framework).

## Overview

The Mina API provides two ways to interact with the backend:

1. **REST API** - Simple HTTP requests for single-shot searches
2. **WebSocket** - Real-time updates during the search process

## Quick Start

### 1. Start the Backend API

```bash
# In the Mina backend repository
python api_server.py
```

The API will be available at `http://localhost:8000`.

### 2. Set Up Frontend Environment

Create a `.env.local` file in your frontend project:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 3. Copy Integration Files

Copy these example files to your frontend project:

```bash
# From Mina/examples/ to your frontend project:
cp examples/api_client.ts your-frontend/lib/api-client.ts
cp examples/useMinaSearch.ts your-frontend/hooks/useMinaSearch.ts
```

### 4. Use in Your Components

```tsx
import { useMinaSearch } from '@/hooks/useMinaSearch';

export default function SearchPage() {
  const { results, loading, error, searchREST } = useMinaSearch();

  const handleSearch = () => {
    searchREST({
      category: 'laptop',
      budget_max: 3000,
      priorities: ['Performance', 'Battery Life'],
      specific_needs: 'For software development'
    });
  };

  return (
    <div>
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Searching...' : 'Search Products'}
      </button>
      
      {results && (
        <div>
          {results.recommendations.map((rec, i) => (
            <ProductCard key={i} recommendation={rec} />
          ))}
        </div>
      )}
    </div>
  );
}
```

## API Reference

### REST API Endpoints

#### Health Check

```typescript
GET /api/health

Response:
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

#### Product Search

```typescript
POST /api/search
Content-Type: application/json

Request:
{
  "category": "laptop" | "furniture" | "appliance",
  "budget_max": number,  // Minimum $500
  "priorities": string[],
  "specific_needs": string (optional)
}

Response:
{
  "recommendations": [
    {
      "product": {
        "name": string,
        "price": number,
        "retailer": string,
        "url": string,
        "specs": object,
        "reviews_summary": string,
        "rating": number
      },
      "confidence_score": number,
      "reasoning": string,
      "pros": string[],
      "cons": string[]
    }
  ],
  "total_products_analyzed": number,
  "search_time_seconds": number
}
```

### WebSocket API

#### Connect

```typescript
ws://localhost:8000/ws
```

#### Send Search Request

```typescript
{
  "type": "search",
  "requirements": {
    "category": "laptop",
    "budget_max": 3000,
    "priorities": ["Performance"],
    "specific_needs": ""
  }
}
```

#### Receive Messages

**Connection Confirmation:**
```typescript
{
  "type": "connection",
  "status": "connected",
  "message": "Connected to Mina API"
}
```

**Progress Updates:**
```typescript
{
  "type": "progress",
  "status": "browsing" | "analyzing" | "scoring",
  "message": string
}
```

**Results:**
```typescript
{
  "type": "results",
  "status": "completed",
  "recommendations": [...],
  "total_products_analyzed": number
}
```

**Error:**
```typescript
{
  "type": "error",
  "status": "failed",
  "message": string
}
```

## Integration Examples

### Using REST API (Simple)

```typescript
import { minaClient } from '@/lib/api-client';

async function searchLaptops() {
  try {
    const results = await minaClient.searchProducts({
      category: 'laptop',
      budget_max: 3000,
      priorities: ['Performance', 'Battery Life']
    });
    
    console.log(`Found ${results.total_products_analyzed} products`);
    results.recommendations.forEach(rec => {
      console.log(`${rec.product.name}: ${rec.confidence_score}% confidence`);
    });
  } catch (error) {
    console.error('Search failed:', error);
  }
}
```

### Using WebSocket (Real-time)

```typescript
import { minaClient } from '@/lib/api-client';

function searchWithProgress() {
  const ws = minaClient.connectWebSocket((message) => {
    switch (message.type) {
      case 'connection':
        console.log('Connected!');
        // Send search request
        minaClient.sendSearchRequest(ws, {
          category: 'laptop',
          budget_max: 3000,
          priorities: ['Performance']
        });
        break;
        
      case 'progress':
        console.log('Progress:', message.message);
        break;
        
      case 'results':
        console.log('Results:', message.recommendations);
        ws.close();
        break;
        
      case 'error':
        console.error('Error:', message.message);
        ws.close();
        break;
    }
  });
}
```

### Using React Hook

```tsx
import { useMinaSearch } from '@/hooks/useMinaSearch';
import { useState } from 'react';

export default function SearchInterface() {
  const { results, loading, error, progress, searchWebSocket } = useMinaSearch();
  const [category, setCategory] = useState('laptop');
  const [budget, setBudget] = useState(3000);
  const [priorities, setPriorities] = useState(['Performance', 'Battery Life']);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    searchWebSocket({
      category: category as 'laptop' | 'furniture' | 'appliance',
      budget_max: budget,
      priorities: priorities,
      specific_needs: ''
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Mina Shopping Agent</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Category</label>
          <select 
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="laptop">Laptop</option>
            <option value="furniture">Furniture</option>
            <option value="appliance">Appliance</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">
            Budget (max: ${budget})
          </label>
          <input
            type="range"
            min="500"
            max="10000"
            step="100"
            value={budget}
            onChange={(e) => setBudget(parseInt(e.target.value))}
            className="w-full"
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Searching...' : 'Search Products'}
        </button>
      </form>
      
      {loading && progress && (
        <div className="mt-4 p-4 bg-blue-50 rounded">
          <p className="text-sm text-blue-800">{progress}</p>
        </div>
      )}
      
      {error && (
        <div className="mt-4 p-4 bg-red-50 rounded">
          <p className="text-sm text-red-800">{error.message}</p>
        </div>
      )}
      
      {results && (
        <div className="mt-6 space-y-4">
          <h2 className="text-2xl font-semibold">
            Found {results.total_products_analyzed} Products
          </h2>
          
          {results.recommendations.map((rec, i) => (
            <div key={i} className="border rounded-lg p-4 shadow-sm">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-xl font-semibold">{rec.product.name}</h3>
                <span className="text-sm font-medium text-green-600">
                  {rec.confidence_score.toFixed(1)}% confidence
                </span>
              </div>
              
              <div className="mb-3">
                <p className="text-lg font-semibold text-gray-900">
                  ${rec.product.price.toLocaleString()}
                </p>
                <p className="text-sm text-gray-600">
                  {rec.product.retailer} • {rec.product.rating}/5.0 ⭐
                </p>
              </div>
              
              <div className="mb-3">
                <h4 className="font-medium mb-1">Strengths:</h4>
                <ul className="list-disc list-inside text-sm text-gray-700">
                  {rec.pros.map((pro, j) => (
                    <li key={j}>{pro}</li>
                  ))}
                </ul>
              </div>
              
              {rec.cons[0] !== "None identified" && (
                <div className="mb-3">
                  <h4 className="font-medium mb-1">Considerations:</h4>
                  <ul className="list-disc list-inside text-sm text-gray-700">
                    {rec.cons.map((con, j) => (
                      <li key={j}>{con}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <a
                href={rec.product.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-2 text-blue-600 hover:underline"
              >
                View Product →
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```typescript
try {
  const results = await minaClient.searchProducts(requirements);
  // Handle success
} catch (error) {
  if (error.message.includes('Invalid category')) {
    // Handle validation error
  } else if (error.message.includes('fetch')) {
    // Handle network error
  } else {
    // Handle other errors
  }
}
```

### 2. Loading States

Provide clear feedback during searches:

```tsx
{loading && (
  <div>
    <Spinner />
    <p>{progress || 'Searching...'}</p>
  </div>
)}
```

### 3. WebSocket Reconnection

Handle WebSocket disconnections:

```typescript
const connectWithRetry = (retries = 3) => {
  const ws = minaClient.connectWebSocket(
    handleMessage,
    (error) => {
      if (retries > 0) {
        setTimeout(() => connectWithRetry(retries - 1), 1000);
      }
    }
  );
};
```

### 4. TypeScript Types

Use the provided TypeScript types for type safety:

```typescript
import type { 
  SearchRequirements, 
  SearchResponse, 
  Recommendation 
} from '@/lib/api-client';
```

### 5. Environment Variables

Always use environment variables for configuration:

```typescript
// .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

// In production:
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

## CORS Configuration

The backend is pre-configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

To add more origins, edit `api_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-production-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing

### Test the API Connection

```typescript
import { minaClient } from '@/lib/api-client';

async function testConnection() {
  try {
    const health = await minaClient.healthCheck();
    console.log('API Status:', health.status);
    console.log('Integrations:', health.integrations);
    return true;
  } catch (error) {
    console.error('API not reachable:', error);
    return false;
  }
}
```

### Mock API for Development

Create a mock client for development without the backend:

```typescript
export class MockMinaClient {
  async searchProducts(requirements: SearchRequirements): Promise<SearchResponse> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      recommendations: [
        {
          product: {
            name: "Mock Laptop",
            price: 2000,
            retailer: "Mock Store",
            url: "https://example.com",
            specs: {},
            reviews_summary: "Great laptop",
            rating: 4.5
          },
          confidence_score: 85,
          reasoning: "Mock reasoning",
          pros: ["Fast", "Good battery"],
          cons: ["Expensive"]
        }
      ],
      total_products_analyzed: 3,
      search_time_seconds: 2.0
    };
  }
}
```

## Troubleshooting

### API Not Reachable

1. Check if the backend is running: `curl http://localhost:8000/api/health`
2. Verify CORS settings in `api_server.py`
3. Check environment variables in `.env.local`

### WebSocket Connection Failed

1. Ensure WebSocket URL uses `ws://` (or `wss://` for HTTPS)
2. Check browser console for CORS errors
3. Verify the backend is accepting WebSocket connections

### Type Errors

1. Make sure TypeScript types are properly imported
2. Update types if the API response structure changes
3. Use type assertions carefully: `data as SearchResponse`

## Next Steps

1. Start the backend: `python api_server.py`
2. Copy integration files to your frontend
3. Test the health endpoint
4. Implement search interface
5. Add error handling and loading states
6. Deploy both frontend and backend

## Support

For questions or issues:
- Backend API: See [START_API.md](START_API.md)
- GitHub Issues: [wildhash/Mina](https://github.com/wildhash/Mina/issues)
