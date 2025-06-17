from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class FakePhysicalNote:
    name: str = 'applications-of-statistical-mechanics'
    title: str = 'Applications of Statistical Mechanics'
    author: str = 'Alex Moss 1'
    category: str = 'physical'
    description: str = 'Starts with basic revision of Statistical Mechanics'
    level: str = '3rd Year Undergraduate'
    filesize: int = 267264
    asset_link: str = '/pdf/Physical/applications_stat_mech.pdf'
    doc_id: int = 99
    tags: List = field(default_factory=lambda: ['mechanics', 'equilibrium'])
    last_modified: datetime = datetime(2003, 12, 9, 0, 0)


@dataclass
class FakeInorganicNote:
    name: str = 'advanced-solid-state'
    title: str = 'Advanced Solid State'
    author: str = 'Alex Moss 2'
    category: str = 'inorganic'
    description: str = 'Only covers the topics I chose to study for - namely Synthesis'
    level: str = '3rd Year Undergraduate'
    filesize: int = 677888
    asset_link: str = '/pdf/Inorganic/solid_state_advanced.pdf'
    doc_id: int = 75
    tags: List = field(default_factory=lambda: [])
    last_modified: datetime = datetime(2003, 11, 20, 0, 0)


@dataclass
class FakeOrganicNote:
    name: str = 'alicyclic-chemistry'
    title: str = 'Alicyclic Chemistry'
    author: str = 'Alex Moss 3'
    category: str = 'organic'
    description: str = 'Basic notes on conformation and reactivity.'
    level: str = '2nd Year Undergraduate'
    filesize: int = 162816
    asset_link: str = '/pdf/Organic/alicyclic.pdf'
    doc_id: int = 82
    tags: List = field(default_factory=lambda: ['reactivity'])
    last_modified: datetime = datetime(2003, 12, 9, 0, 0)
