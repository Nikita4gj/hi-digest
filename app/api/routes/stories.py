from fastapi import APIRouter, Request

from app.models import Story

router = APIRouter()

#* Наши routes для api Hacker News
@router.get("/stories")
async def get_stories(request: Request, count: int = 10) -> list[int]:
    cli = request.app.state.hn_cli
    return await cli.get_topstories_ids(count)

@router.get("/story/{story_id}")
async def get_story_by_id(request: Request, story_id: int) -> Story | None:
    cli = request.app.state.hn_cli
    return await cli.get_story_by_id(story_id)