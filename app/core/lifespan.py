from contextlib import asynccontextmanager
from httpx import AsyncClient
from fastapi import FastAPI

from app.clients import HNClient

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