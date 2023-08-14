from dataclasses import dataclass
from typing import Union

import requests


@dataclass
class StoryPart:
    id: str
    title: str
    url: str
    photoUrl: str
    groupId: Union[str, None] = None

    def __post_init__(self):
        if isinstance(self.id, int):
            self.id = str(self.id)


@dataclass
class Story:
    id: str
    url: str
    cover: str
    title: str
    numParts: int
    parts: list[StoryPart]

    def __post_init__(self):
        if len(self.parts) > 0 and isinstance(self.parts[0], dict):
            self.parts = [StoryPart(**it) for it in self.parts]


def _get(url: str, add_base: bool = True, **kwargs):
    return requests.get(f'https://api.wattpad.com/api/v3/{url}' if add_base else url,
                        **kwargs, headers={'User-Agent': 'curl/7.88.1-DEV'})


def story_by_id(id: str):
    response = _get(f'stories/{id}', params={
        'fields': 'id,url,cover,title,numParts,parts(id,title,photoUrl,url)'
    }).json()

    story = Story(**response)
    return story


def story_part_text(part: Union[str, StoryPart]):
    if isinstance(part, StoryPart):
        part = str(part.id)

    response = _get(f'https://api.wattpad.com/apiv2/storytext', add_base=False, params={
        'id': part
    })

    return response.text


def part_by_id(id: str):
    response = _get(f'story_parts/{id}', params={
        'fields': 'id,title,url,photoUrl,groupId'
    }).json()

    part = StoryPart(**response)
    return part
