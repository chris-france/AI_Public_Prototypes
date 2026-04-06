"""FastAPI backend for the Personal Demo Launcher."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from process_manager import cleanup_all
from routers.demos import router as demos_router
from routers.feedback import router as feedback_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cleanup all managed processes on shutdown."""
    yield
    cleanup_all()


app = FastAPI(title="Personal Demo Launcher", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(demos_router)
app.include_router(feedback_router)
