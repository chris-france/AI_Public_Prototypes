"""FastAPI backend for the Model Security Scanner."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers.scanner import router as scanner_router

app = FastAPI(title="Model Security Scanner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scanner_router)

init_db()
