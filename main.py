from fastapi import FastAPI

from  hn_client import HNClient
from httpx import AsyncClient

from contextlib import asynccontextmanager

@asynccontextmanager 
async def lifespan(app: FastAPI):
    app.state.hn_cli = HNClient(AsyncClient())
    try:
        yield
    finally:
        await app.state.hn_cli.client.aclose()
        
        
app = FastAPI(lifespan=lifespan)

@app.get("/stories")
async def get_stories(count: int = 10) -> list[int]:
    cli = app.state.hn_cli
    return await cli.get_topstories_id(count)
    
    
    
    


