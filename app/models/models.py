from dataclasses import dataclass

from typing import Any

@dataclass
class Story:
    """
    Класс "истории" с Hacker News
    
    ### _Overview_:
        - id: int
        - title: str
        - author: str
        - url: str
        - score: int
    """
    id: int
    title: str
    author: str
    url: str
    score: int
    def to_dict(self) -> dict[str, Any]:
        return self.__dict__;


