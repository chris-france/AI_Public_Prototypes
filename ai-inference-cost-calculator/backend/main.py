"""FastAPI backend for the AI Inference Cost Calculator."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.calculator import router as calculator_router
from routers.feedback import router as feedback_router

app = FastAPI(title="AI Inference Cost Calculator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator_router)
app.include_router(feedback_router)
