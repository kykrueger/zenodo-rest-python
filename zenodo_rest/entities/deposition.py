from typing import Optional, TypeVar
import os

T = TypeVar('Deposition')

from pydantic import BaseModel
import requests

from zenodo_rest.entities.deposition_file import DepositionFile
from zenodo_rest.entities.metadata import Metadata


class Deposition(BaseModel):
    created: str
    doi: Optional[str]
    doi_url: Optional[str]
    files: Optional[list[DepositionFile]]
    id: str
    links: dict
    metadata: Metadata
    modified: str
    owner: int
    record_id: int
    record_url: Optional[str]
    state: str
    submitted: bool
    title: str

    @staticmethod
    def retrieve(
            deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> T:
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.get(
            f"{base_url}/api/deposit/depositions/{deposition_id}",
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def refresh(self, token: str = None) -> Optional[T]:
        return Deposition.retrieve(self.id, token)

    def get_latest(self, token: str = None) -> Optional[T]:

        deposition: Deposition = self.refresh(token)
        latest_url = deposition.links.get("latest", None)
        if latest_url is None:
            return None
        latest_id = latest_url.rsplit('/', 1)[1]
        return Deposition.retrieve(latest_id)

    def get_latest_draft(self, token: str = None) -> Optional[T]:
        deposition: Deposition = self.refresh(token)
        latest_draft_url = deposition.links.get("latest_draft", None)
        if latest_draft_url is None:
            return None

        if token is None:
            token = os.getenv("ZENODO_TOKEN")

        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(
            latest_draft_url,
            headers=header,
        )
        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def get_bucket(self) -> str:
        return self.links.get('bucket')
