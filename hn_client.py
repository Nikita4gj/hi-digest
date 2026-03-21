from httpx import AsyncClient
from httpx import _exceptions as httpx_exc

from typing import Any

from models import Story


class HNClient:
    
    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_topstories_id(self, count: int = 10) -> list[int]:
        try:
            if not isinstance(count, int):
                raise TypeError(f"Expected type is 'int' not {type(count)}")
            if count <=0:
                raise ValueError("Expected count which is > 0")
            
            response = await self.client.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
                
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")

            if "application/json" not in content_type:
                raise TypeError("Unexpected content type")

            data = response.json()

            if not isinstance(data, list) :
                raise TypeError("Expected list from API")
            
            return data[:count]
        
        except httpx_exc.RequestError:
            raise

    async def _fetch_story_json(self, id: int) -> dict[str, Any]:
        try:
            if not isinstance(id, int):
                raise TypeError(f"Expected type is 'int' not {type(id)}")
            
            response = await self.client.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json", timeout=10)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")

            if "application/json" not in content_type:
                raise TypeError("Unexpected content type")
            
            data = response.json()

            if not isinstance(data, dict):
                raise TypeError("Expected dict from API")
            
            return data

        except httpx_exc.RequestError:
            raise

    async def get_story_by_id(self, id: int) -> Story | None:
        data = await self._fetch_story_json(id)
        return self._parse_story(data)        
    
    @staticmethod
    def _parse_story(data: dict[str, Any]) -> Story | None:
        if data.get("type", "") != "story":
                return None
            
        story_id = data.get("id")
        if not isinstance(story_id, int):
            return None
            
        title = data.get("title")
        if not isinstance(title, str):
            return None
            
        author = data.get("by")
        if not isinstance(author, str):
            return None
            
        url = data.get("url")
        if not isinstance(url, str):
            return None
        
        score = data.get("score")
        if not isinstance(score, int):
            return None
        
        return Story(story_id, title, author, url, score)


