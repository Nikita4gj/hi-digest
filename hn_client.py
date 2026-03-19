from requests import get
from requests import exceptions

from typing import Any

from models import Story

def get_topstories_id(count: int = 10) -> list[int]:
    try:
        if not isinstance(count, int):
            raise TypeError(f"Expected type is 'int' not {type(count)}")
        if count <=0:
            raise ValueError("Expected count which is > 0")
        
        response = get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")

        if "application/json" not in content_type:
            raise TypeError("Unexpected content type")

        data = response.json()

        if not isinstance(data, list) :
            raise TypeError("Expected list from API")
        
        return data[:count]
    
    except exceptions.RequestException as exeption:
        raise

def _fetch_story_json(id: int) -> dict[str, Any]:
    try:
        if not isinstance(id, int):
            raise TypeError(f"Expected type is 'int' not {type(id)}")
        
        response = get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")

        if "application/json" not in content_type:
            raise TypeError("Unexpected content type")
        
        data = response.json()

        if not isinstance(data, dict):
            raise TypeError("Expected dict from API")
        
        return data

    except exceptions.RequestException as exeption:
        raise


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

def get_story_by_id(id: int) ->Story | None:
    data = _fetch_story_json(id)
    return _parse_story(data)    


