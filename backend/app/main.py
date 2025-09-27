"""
Main FastAPI application for the Autonomous Recruitment Platform.
This module initializes the FastAPI app and configures startup/shutdown events.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routes import agent_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    print("Starting Autonomous Recruitment Platform...")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
    
    yield
    
    # Shutdown
    print("Shutting down Autonomous Recruitment Platform...")


def create_app() -> FastAPI:
    """
    Initializes and returns the main FastAPI application instance.
    """
    app = FastAPI(
        title="Autonomous Recruitment Platform",
        description="Backend API for managing autonomous AI recruitment agents",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Mount agent routes
    app.include_router(agent_routes.router, prefix="/api/v1", tags=["agents"])
    
    return app


# Create the FastAPI application instance
app = create_app()


@app.get("/")
async def root():
    """
    Root endpoint to verify the application is running.
    """
    return {"message": "Autonomous Recruitment Platform API is running"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {"status": "healthy", "service": "autonomous-recruitment-platform"}
