import hn_client
import asyncio

from pprint import pprint

from httpx import AsyncClient

from models import Story

async def get_top_story_ids(ids:list[int])->list[Story | None]:  
    
    async with AsyncClient() as cli:
        tasks = [
            asyncio.create_task(hn_client.get_story_by_id(cli, story_id))
            for story_id in ids
        ]   
        
        return await asyncio.gather(*tasks)
        
async def loop():
    ids = await hn_client.get_topstories_id(5)
    
    stories  = await get_top_story_ids(ids)
    
    pprint(stories)
    


if __name__ == "__main__":
    asyncio.run(loop())
    


