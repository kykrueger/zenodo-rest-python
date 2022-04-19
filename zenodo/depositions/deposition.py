from typing import Optional

from pydantic import BaseModel

from zenodo.entities.metadata import Metadata
from zenodo.entities.zenodo_file import ZenodoFile


class Deposition(BaseModel):
    created: str
    doi: str
    doi_url: str
    files: list[ZenodoFile]
    id: int
    metadata: Metadata
    modified: str
    owner: int
    record_id: int
    record_url: Optional[str] = None
    state: str
    submitted: bool
    title: str
