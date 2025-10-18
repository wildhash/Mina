/**
 * React Hook for Mina Search
 * 
 * Custom React hook for managing product search state and interactions
 * with the Mina API.
 * 
 * Usage in Next.js:
 * 1. Copy this file to your frontend project: hooks/useMinaSearch.ts
 * 2. Copy api_client.ts to lib/api-client.ts
 * 3. Use the hook in your components
 */

import { useState, useCallback, useEffect } from 'react';
import { 
  MinaAPIClient, 
  SearchRequirements, 
  SearchResponse,
  Recommendation,
  WSMessage 
} from '../lib/api-client';

export interface UseMinaSearchResult {
  // State
  results: SearchResponse | null;
  loading: boolean;
  error: Error | null;
  progress: string | null;
  
  // Actions
  searchREST: (requirements: SearchRequirements) => Promise<void>;
  searchWebSocket: (requirements: SearchRequirements) => void;
  clearResults: () => void;
  clearError: () => void;
}

/**
 * Custom hook for managing Mina product search
 * 
 * @returns Search state and actions
 * 
 * @example
 * ```tsx
 * function SearchComponent() {
 *   const { results, loading, error, searchREST } = useMinaSearch();
 * 
 *   const handleSearch = () => {
 *     searchREST({
 *       category: 'laptop',
 *       budget_max: 3000,
 *       priorities: ['Performance', 'Battery Life']
 *     });
 *   };
 * 
 *   return (
 *     <div>
 *       <button onClick={handleSearch} disabled={loading}>
 *         {loading ? 'Searching...' : 'Search'}
 *       </button>
 *       {error && <p>Error: {error.message}</p>}
 *       {results && (
 *         <div>
 *           <h3>Found {results.total_products_analyzed} products</h3>
 *           {results.recommendations.map((rec, i) => (
 *             <ProductCard key={i} recommendation={rec} />
 *           ))}
 *         </div>
 *       )}
 *     </div>
 *   );
 * }
 * ```
 */
export function useMinaSearch(): UseMinaSearchResult {
  const [client] = useState(() => new MinaAPIClient());
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [progress, setProgress] = useState<string | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  // Clean up WebSocket on unmount
  useEffect(() => {
    return () => {
      if (ws) {
        ws.onmessage = null;
        ws.onerror = null;
        ws.onclose = null;
        ws.close();
      }
    };
  }, [ws]);

  /**
   * Perform search using REST API (simple, single response)
   */
  const searchREST = useCallback(async (requirements: SearchRequirements) => {
    setLoading(true);
    setError(null);
    setProgress('Starting search...');

    try {
      const data = await client.searchProducts(requirements);
      setResults(data);
      setProgress(null);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Search failed');
      setError(error);
      setProgress(null);
    } finally {
      setLoading(false);
    }
  }, [client]);

  /**
   * Perform search using WebSocket (real-time progress updates)
   */
  const searchWebSocket = useCallback((requirements: SearchRequirements) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setProgress('Connecting...');

    // Close existing connection if any
    if (ws) {
      ws.onmessage = null;
      ws.onerror = null;
      ws.onclose = null;
      ws.close();
    }

    // Create new WebSocket connection
    const newWs = client.connectWebSocket(
      (message: WSMessage) => {
        switch (message.type) {
          case 'connection':
            setProgress('Connected - Starting search...');
            // Send search request after connection
            client.sendSearchRequest(newWs, requirements);
            break;

          case 'progress':
            setProgress(message.message || 'Processing...');
            break;

          case 'results':
            if (message.recommendations) {
              setResults({
                recommendations: message.recommendations,
                total_products_analyzed: message.total_products_analyzed || 0,
              });
            }
            setProgress(null);
            setLoading(false);
            break;

          case 'error':
            setError(new Error(message.message || 'Search failed'));
            setProgress(null);
            setLoading(false);
            break;

          default:
            break;
        }
      },
      (error) => {
        setError(new Error('WebSocket connection failed'));
        setProgress(null);
        setLoading(false);
      }
    );

    setWs(newWs);
  }, [client]); // Removed ws from dependencies to avoid recreation

  /**
   * Clear search results
   */
  const clearResults = useCallback(() => {
    setResults(null);
    setProgress(null);
  }, []);

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    results,
    loading,
    error,
    progress,
    searchREST,
    searchWebSocket,
    clearResults,
    clearError,
  };
}

/**
 * Example component using the hook with WebSocket:
 * 
 * ```tsx
 * import { useMinaSearch } from '@/hooks/useMinaSearch';
 * 
 * export default function SearchPage() {
 *   const { results, loading, error, progress, searchWebSocket } = useMinaSearch();
 *   
 *   const handleSearch = () => {
 *     searchWebSocket({
 *       category: 'laptop',
 *       budget_max: 3000,
 *       priorities: ['Performance', 'Battery Life'],
 *       specific_needs: 'For software development'
 *     });
 *   };
 *   
 *   return (
 *     <div>
 *       <button onClick={handleSearch} disabled={loading}>
 *         Search Products
 *       </button>
 *       
 *       {loading && (
 *         <div>
 *           <Spinner />
 *           <p>{progress}</p>
 *         </div>
 *       )}
 *       
 *       {error && (
 *         <Alert variant="error">
 *           {error.message}
 *         </Alert>
 *       )}
 *       
 *       {results && (
 *         <div>
 *           <h2>Found {results.total_products_analyzed} Products</h2>
 *           {results.recommendations.map((rec, i) => (
 *             <RecommendationCard
 *               key={i}
 *               rank={i + 1}
 *               recommendation={rec}
 *             />
 *           ))}
 *         </div>
 *       )}
 *     </div>
 *   );
 * }
 * ```
 */
