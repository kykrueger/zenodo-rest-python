from typing import Optional

from pydantic import BaseModel

from zenodo.entities.deposition_file import DepositionFile
from zenodo.entities.metadata import Metadata


class Deposition(BaseModel):
    created: str
    doi: Optional[str]
    doi_url: Optional[str]
    files: Optional[list[DepositionFile]]
    id: int
    links: dict
    metadata: Metadata
    modified: str
    owner: int
    record_id: int
    record_url: Optional[str]
    state: str
    submitted: bool
    title: str
