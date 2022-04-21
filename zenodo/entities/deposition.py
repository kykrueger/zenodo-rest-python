import os
from pathlib import Path
from typing import Optional, TypeVar

import requests
from pydantic import BaseModel

from zenodo.entities.deposition_file import DepositionFile
from zenodo.entities.metadata import Metadata

T = TypeVar("T", bound="Deposition")


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

    @staticmethod
    def create(
        metadata: Metadata = Metadata(),
        prereserve_doi: Optional[bool] = None,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> T:
        """
        Create a deposition on the server, but do not publish it.
        """

        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")

        if prereserve_doi is True:
            metadata.prereserve_doi = True

        header = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{base_url}/api/deposit/depositions",
            json={"metadata": metadata.dict(exclude_none=True)},
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    @staticmethod
    def retrieve(
        depositionId: int, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> T:

        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.get(
            f"{base_url}/api/deposit/depositions/{depositionId}",
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    @staticmethod
    def static_update_metadata(
        deposition_id: int,
        metadata: Metadata,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> T:
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.put(
            f"{base_url}/api/deposit/depositions/{deposition_id}",
            json={"metadata": metadata.dict(exclude_none=True)},
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def update_metadata(
        self,
        metadata: Metadata,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> T:
        return Deposition.static_update_metadata(self.id, metadata, token, base_url)

    @staticmethod
    def static_delete_remote(
        deposition_id: int, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> requests.Response:
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.delete(
            f"{base_url}/api/deposit/depositions/{deposition_id}",
            headers=header,
        )

        return response

    def delete_remote(
        self, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> requests.Response:
        return Deposition.static_delete_remote(self.id, token, base_url)

    def upload_file(
        self, path_to_file: str, token: Optional[str] = None
    ) -> requests.Response:
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        bucket_url = self.links["bucket"]
        path = Path(path_to_file)
        header = {"Authorization": f"Bearer {token}"}
        with open(path_to_file, "rb") as fp:
            r = requests.put(
                f"{bucket_url}/{path.name}",
                data=fp,
                headers=header,
            )
        r.raise_for_status()
        return r
