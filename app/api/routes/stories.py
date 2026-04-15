from fastapi import APIRouter, Depends

from .depends import _get_hn_client
from app.clients import HNClient
from app.models import Story

router = APIRouter(tags=["stories"])

#* Наши routes для api Hacker News
@router.get("/stories", response_model = list[int])
async def get_stories(count: int = 10, cli: HNClient = Depends(_get_hn_client)) -> list[int]:
    return await cli.get_topstories_ids(count)

@router.get("/story/{story_id}", response_model = Story | None)
async def get_story_by_id(story_id: int, cli: HNClient = Depends(_get_hn_client)) -> Story | None:
    return await cli.get_story_by_id(story_id)