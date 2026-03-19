import hn_client
import asyncio

from pprint import pprint

from models import Story

async def get_top_story_ids(ids:list[int])->list[Story | None]:
    tasks = []
    for story_id in ids:
        tasks.append(asyncio.to_thread(hn_client.get_story_by_id, story_id))
    
    return await asyncio.gather(*tasks)
        

if __name__ == "__main__":
    ids = hn_client.get_topstories_id(5)

    stories = asyncio.run(get_top_story_ids(ids))

    pprint(stories)


