from app.clients import HNClient
from httpx import AsyncClient

from contextlib import asynccontextmanager

from fastapi import FastAPI

@asynccontextmanager 
async def lifespan(app: FastAPI):
    """
    Lifespan для приложения
    """
    app.state.hn_cli = HNClient(AsyncClient())
    try:
        yield
    finally:
        await app.state.hn_cli.client.aclose()