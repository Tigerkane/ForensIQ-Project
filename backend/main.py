from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import models
from database.database import engine

# Create SQLite tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ForensIQ API", description="Offline Investigation Intelligence API")

from api.router import router as api_router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "ForensIQ CPU-First Backend is running."}

@app.get("/health")
def health_check():
    return {"status": "offline_system_active"}
