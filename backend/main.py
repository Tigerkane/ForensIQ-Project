from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import models
from database.database import engine
from api.router import router as api_router

# Create SQLite tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ForensIQ API", description="Offline Investigation Intelligence API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://forensiq.vercel.app", "https://forens-iq-project.vercel.app"],
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
