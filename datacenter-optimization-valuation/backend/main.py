"""FastAPI backend for the DC Optimization & Valuation Tool."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.deployment import router as deployment_router
from routers.valuation import router as valuation_router
from routers.benchmarks import router as benchmarks_router

app = FastAPI(title="DC Optimization & Valuation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deployment_router)
app.include_router(valuation_router)
app.include_router(benchmarks_router)
