from httpx import AsyncClient
from httpx import _exceptions as httpx_exc

from typing import Any

from app.models import Story

class HNClient:
    """
    Класс для работы с api Hacker News
    """
    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_topstories_ids(self, count: int = 10) -> list[int]:
        """
        Возвращает первые _count_ id историй с Hacker News

        Args:
            _count_ (int, optional): Количество id которые надо вернуть. Дефолт 10.

        Raises:
            TypeError: _count_ не int
            ValueError: _count_ <= 0
            TypeError: Ответ пришел не в "application/json"
            TypeError: Вернулся не list, а что-то другое

        Returns:
            list[int]: Список top истоий длинной в _ount_
        """
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

    async def _fetch_story_json(self, story_id: int) -> dict[str, Any]:
        try:
            if not isinstance(story_id, int):
                raise TypeError(f"Expected type is 'int' not {type(story_id)}")
            
            response = await self.client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10)
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

    async def get_story_by_id(self, story_id: int) -> Story | None:
        """Возвращает Story по id, если история некорректная
        то возвращает None

        Args:
            story_id (int): _id_ истории, которую хотим получить

        Returns:
            Story|None: Валидная история или None
        """
        data = await self._fetch_story_json(story_id)
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


