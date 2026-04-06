"""FastAPI backend for the Datacenter Demand Simulator."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.simulation import router as simulation_router
from routers.feedback import router as feedback_router

app = FastAPI(title="Datacenter Demand Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation_router)
app.include_router(feedback_router)
