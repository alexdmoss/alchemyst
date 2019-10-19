from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Note:
    name: str
    title: str
    author: str
    category: str
    tags: List
    description: str
    level: str
    filesize: int
    asset_link: str
    doc_id: int
    last_modified: datetime
