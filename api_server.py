"""
FastAPI Server for Mina Shopping Agent

This module provides a REST API and WebSocket interface for the Mina agent,
enabling frontend integration and real-time product search functionality.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
except ImportError:
    print("FastAPI not installed. Install with: pip install -r requirements.txt")
    exit(1)

from mina_agent import MinaAgent, ProductOption, Recommendation


# Pydantic models for API requests and responses
class SearchRequirements(BaseModel):
    """User requirements for product search."""
    category: str = Field(..., description="Product category: laptop, furniture, or appliance")
    budget_max: float = Field(..., description="Maximum budget in dollars", ge=500)
    priorities: List[str] = Field(..., description="List of user priorities")
    specific_needs: Optional[str] = Field(default="", description="Specific requirements or features")


class ProductOptionResponse(BaseModel):
    """Product option response model."""
    name: str
    price: float
    retailer: str
    url: str
    specs: Dict[str, Any]
    reviews_summary: str
    rating: float


class RecommendationResponse(BaseModel):
    """Recommendation response model."""
    product: ProductOptionResponse
    confidence_score: float
    reasoning: str
    pros: List[str]
    cons: List[str]


class SearchResponse(BaseModel):
    """Complete search response with recommendations."""
    recommendations: List[RecommendationResponse]
    total_products_analyzed: int
    search_time_seconds: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    integrations: Dict[str, bool]


# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await self.send_message(message, connection)


# Initialize connection manager
manager = ConnectionManager()


# Lifespan context manager for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    # Startup
    print("Starting Mina API Server...")
    print("Initializing Mina agent...")
    app.state.agent = MinaAgent()
    print("✓ Mina agent initialized")
    
    yield
    
    # Shutdown
    print("Shutting down Mina API Server...")


# Create FastAPI app
app = FastAPI(
    title="Mina Shopping Agent API",
    description="AI Shopping Concierge API for high-end purchases",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def product_option_to_dict(product: ProductOption) -> Dict[str, Any]:
    """Convert ProductOption to dictionary."""
    return {
        "name": product.name,
        "price": product.price,
        "retailer": product.retailer,
        "url": product.url,
        "specs": product.specs,
        "reviews_summary": product.reviews_summary,
        "rating": product.rating
    }


def recommendation_to_dict(rec: Recommendation) -> Dict[str, Any]:
    """Convert Recommendation to dictionary."""
    return {
        "product": product_option_to_dict(rec.product),
        "confidence_score": rec.confidence_score,
        "reasoning": rec.reasoning,
        "pros": rec.pros,
        "cons": rec.cons
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Mina Shopping Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "search": "/api/search (POST)",
            "websocket": "/ws"
        }
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify API status and integrations."""
    agent = app.state.agent
    
    integrations = {
        "claude": agent.claude_client is not None,
        "browser_use": agent.browser is not None,
        "daytona": agent.daytona is not None,
    }
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        integrations=integrations
    )


@app.post("/api/search", response_model=SearchResponse, tags=["Search"])
async def search_products(requirements: SearchRequirements):
    """
    Search for products based on user requirements.
    
    This endpoint performs a complete product search workflow:
    1. Browse multiple retailers
    2. Analyze products with AI
    3. Calculate confidence scores
    4. Generate personalized recommendations
    
    Args:
        requirements: User search requirements including category, budget, and priorities
        
    Returns:
        SearchResponse with ranked recommendations
    """
    # Validate category
    valid_categories = ["laptop", "furniture", "appliance"]
    if requirements.category.lower() not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )
    
    agent = app.state.agent
    
    # Convert requirements to dict
    req_dict = {
        "category": requirements.category.lower(),
        "budget_max": requirements.budget_max,
        "priorities": requirements.priorities,
        "specific_needs": requirements.specific_needs or ""
    }
    
    # Execute search workflow
    import time
    start_time = time.time()
    
    # Step 1: Browse retailers
    products = agent.browse_retailers(req_dict)
    
    if not products:
        return SearchResponse(
            recommendations=[],
            total_products_analyzed=0,
            search_time_seconds=time.time() - start_time
        )
    
    # Step 2: Analyze with Claude
    analyses = agent.analyze_with_claude(products, req_dict)
    
    # Step 3: Calculate confidence scores
    confidence_scores = agent.calculate_confidence_scores(products, analyses)
    
    # Step 4: Generate recommendations
    recommendations = agent.generate_recommendations(products, analyses, confidence_scores)
    
    search_time = time.time() - start_time
    
    # Convert recommendations to response format
    recommendations_response = [
        RecommendationResponse(
            product=ProductOptionResponse(**product_option_to_dict(rec.product)),
            confidence_score=rec.confidence_score,
            reasoning=rec.reasoning,
            pros=rec.pros,
            cons=rec.cons
        )
        for rec in recommendations
    ]
    
    return SearchResponse(
        recommendations=recommendations_response,
        total_products_analyzed=len(products),
        search_time_seconds=round(search_time, 2)
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time product search updates.
    
    Clients can connect to receive live updates during the search process,
    including progress notifications and intermediate results.
    """
    await manager.connect(websocket)
    
    try:
        # Send welcome message
        await manager.send_message({
            "type": "connection",
            "status": "connected",
            "message": "Connected to Mina API"
        }, websocket)
        
        while True:
            # Receive data from client
            data = await websocket.receive_json()
            
            if data.get("type") == "search":
                try:
                    # Parse requirements
                    requirements = data.get("requirements", {})
                    
                    # Send progress update
                    await manager.send_message({
                        "type": "progress",
                        "status": "started",
                        "message": "Starting product search..."
                    }, websocket)
                    
                    agent = app.state.agent
                    
                    req_dict = {
                        "category": requirements.get("category", "laptop"),
                        "budget_max": requirements.get("budget_max", 3000),
                        "priorities": requirements.get("priorities", []),
                        "specific_needs": requirements.get("specific_needs", "")
                    }
                    
                    # Browse retailers
                    await manager.send_message({
                        "type": "progress",
                        "status": "browsing",
                        "message": "Browsing multiple retailers..."
                    }, websocket)
                    
                    products = agent.browse_retailers(req_dict)
                    
                    # Analyze products
                    await manager.send_message({
                        "type": "progress",
                        "status": "analyzing",
                        "message": f"Analyzing {len(products)} products..."
                    }, websocket)
                    
                    analyses = agent.analyze_with_claude(products, req_dict)
                    
                    # Calculate confidence
                    await manager.send_message({
                        "type": "progress",
                        "status": "scoring",
                        "message": "Calculating confidence scores..."
                    }, websocket)
                    
                    confidence_scores = agent.calculate_confidence_scores(products, analyses)
                    
                    # Generate recommendations
                    recommendations = agent.generate_recommendations(
                        products, analyses, confidence_scores
                    )
                    
                    # Send final results
                    recommendations_data = [
                        recommendation_to_dict(rec) for rec in recommendations
                    ]
                    
                    await manager.send_message({
                        "type": "results",
                        "status": "completed",
                        "recommendations": recommendations_data,
                        "total_products_analyzed": len(products)
                    }, websocket)
                    
                except Exception as e:
                    await manager.send_message({
                        "type": "error",
                        "status": "failed",
                        "message": str(e)
                    }, websocket)
            
            elif data.get("type") == "ping":
                # Respond to ping
                await manager.send_message({
                    "type": "pong",
                    "message": "Server is alive"
                }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "false").lower() == "true"
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║          Mina Shopping Agent API Server                  ║
╚══════════════════════════════════════════════════════════╝

Starting server at: http://{host}:{port}

API Endpoints:
  • Health Check: http://localhost:{port}/api/health
  • Product Search: http://localhost:{port}/api/search
  • WebSocket: ws://localhost:{port}/ws

API Documentation:
  • Swagger UI: http://localhost:{port}/docs
  • ReDoc: http://localhost:{port}/redoc

Press CTRL+C to stop the server
""")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
