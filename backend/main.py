from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routes import router as api_router
from api.auth_routes import router as auth_router
from services.database import connect_to_mongo, close_mongo_connection
import os
print("🔥 APP STARTING...")
print("PORT:", os.getenv("PORT"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle events."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="AI Cyber Security API",
    description="API for detecting fake news, scam messages, and phishing URLs. Includes user auth.",
    version="2.0.0",
    lifespan=lifespan)

origins = [
    "https://cybershield-project-git-main-mannavaharika45s-projects.vercel.app",
    "https://cybershield-project.vercel.app"
]

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(api_router, prefix="/api", tags=["Detection"])


@app.get("/")
def read_root():
    return {"message": "Welcome to CyberShield API v2.0", "status": "online"}
