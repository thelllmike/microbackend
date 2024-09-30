from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

# Import routers from the routers folder
from routers import user, reviews, tickets, features, equipments, predict ,predictiondetails

import logging

# Configure logging with more detailed formatting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My Application",
    description="An application with multiple routers",
    version="1.0.0",
)

# Initialize database and create tables
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing the database...")
    init_db()
    logger.info("Database initialized.")

# Include CORS middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
router_list = [
    (user.router, "/auth", ["auth"]),
    (reviews.router, "/review", ["review"]),
    (tickets.router, "/ticket", ["ticket"]),
    (features.router, "/feature", ["feature"]),
    (equipments.router, "/equipment", ["equipment"]),
    (predict.router, "/predict", ["predict"]),
    (predictiondetails.router, "/details", ["details"]),
]

for router, prefix, tags in router_list:
    app.include_router(router, prefix=prefix, tags=tags)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )