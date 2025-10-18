/**
 * TypeScript API Client for Mina Shopping Agent
 * 
 * This client can be used in Next.js or any TypeScript/JavaScript frontend
 * to communicate with the Mina API backend.
 * 
 * Usage in Next.js:
 * 1. Copy this file to your frontend project: lib/api-client.ts
 * 2. Set NEXT_PUBLIC_API_URL in .env.local (defaults to http://localhost:8000)
 * 3. Import and use the client in your components
 */

// Types for API requests and responses
export interface SearchRequirements {
  category: 'laptop' | 'furniture' | 'appliance';
  budget_max: number;
  priorities: string[];
  specific_needs?: string;
}

export interface ProductOption {
  name: string;
  price: number;
  retailer: string;
  url: string;
  specs: Record<string, any>;
  reviews_summary: string;
  rating: number;
}

export interface Recommendation {
  product: ProductOption;
  confidence_score: number;
  reasoning: string;
  pros: string[];
  cons: string[];
}

export interface SearchResponse {
  recommendations: Recommendation[];
  total_products_analyzed: number;
  search_time_seconds?: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  integrations: {
    claude: boolean;
    browser_use: boolean;
    daytona: boolean;
  };
}

// WebSocket message types
export interface WSMessage {
  type: 'connection' | 'progress' | 'results' | 'error' | 'pong';
  status?: string;
  message?: string;
  recommendations?: Recommendation[];
  total_products_analyzed?: number;
}

/**
 * Main API client for Mina Shopping Agent
 */
export class MinaAPIClient {
  private baseUrl: string;
  private wsUrl: string;

  constructor() {
    // Use environment variable or fallback to localhost
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    this.wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
  }

  /**
   * Check API server health and integration status
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/api/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Search for products based on requirements
   */
  async searchProducts(requirements: SearchRequirements): Promise<SearchResponse> {
    const response = await fetch(`${this.baseUrl}/api/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requirements),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Search failed');
    }

    return response.json();
  }

  /**
   * Connect to WebSocket for real-time search updates
   * 
   * @param onMessage - Callback for received messages
   * @param onError - Optional error callback
   * @returns WebSocket instance
   */
  connectWebSocket(
    onMessage: (data: WSMessage) => void,
    onError?: (error: Event) => void
  ): WebSocket {
    const ws = new WebSocket(`${this.wsUrl}/ws`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) {
        onError(error);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return ws;
  }

  /**
   * Send a search request through WebSocket for real-time updates
   * 
   * @param ws - Active WebSocket connection
   * @param requirements - Search requirements
   */
  sendSearchRequest(ws: WebSocket, requirements: SearchRequirements): void {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'search',
        requirements,
      }));
    } else {
      throw new Error('WebSocket is not connected');
    }
  }

  /**
   * Send a ping to keep the connection alive
   * 
   * @param ws - Active WebSocket connection
   */
  sendPing(ws: WebSocket): void {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'ping' }));
    }
  }
}

// Export singleton instance for convenience
export const minaClient = new MinaAPIClient();

/**
 * Example usage in a React component:
 * 
 * import { minaClient, SearchRequirements } from '@/lib/api-client';
 * 
 * const MyComponent = () => {
 *   const [results, setResults] = useState(null);
 *   const [loading, setLoading] = useState(false);
 * 
 *   const handleSearch = async () => {
 *     setLoading(true);
 *     try {
 *       const requirements: SearchRequirements = {
 *         category: 'laptop',
 *         budget_max: 3000,
 *         priorities: ['Performance', 'Battery Life'],
 *         specific_needs: 'For software development'
 *       };
 *       
 *       const data = await minaClient.searchProducts(requirements);
 *       setResults(data);
 *     } catch (error) {
 *       console.error('Search failed:', error);
 *     } finally {
 *       setLoading(false);
 *     }
 *   };
 * 
 *   return (
 *     <div>
 *       <button onClick={handleSearch} disabled={loading}>
 *         {loading ? 'Searching...' : 'Search Products'}
 *       </button>
 *       {results && (
 *         <div>
 *           {results.recommendations.map((rec, i) => (
 *             <div key={i}>
 *               <h3>{rec.product.name}</h3>
 *               <p>Confidence: {rec.confidence_score}%</p>
 *               <p>Price: ${rec.product.price}</p>
 *             </div>
 *           ))}
 *         </div>
 *       )}
 *     </div>
 *   );
 * };
 */
