from dataclasses import dataclass
from datetime import datetime


@dataclass
class FakeNote:
    name: str = 'applications-of-statistical-mechanics'
    title: str = 'Applications of Statistical Mechanics'
    author: str = 'Alex Moss'
    category: str = 'physical'
    description: str = 'Starts with basic revision of Statistical Mechanics'
    level: str = '3rd Year Undergraduate'
    filesize: int = 267264
    asset_link: str = '/pdf/Physical/applications_stat_mech.pdf'
    doc_id: int = 99
    last_modified: datetime = datetime(2003, 12, 9, 0, 0)
