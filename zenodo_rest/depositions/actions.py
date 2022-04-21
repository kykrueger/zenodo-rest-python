import os
from pathlib import Path
from typing import Optional

import requests

from zenodo_rest.entities.metadata import Metadata
from zenodo_rest.entities.deposition import Deposition
from zenodo_rest.entities.bucket_file import BucketFile


def create(
        metadata: Metadata = Metadata(),
        prereserve_doi: Optional[bool] = None,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
) -> Deposition:
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


def retrieve(
        deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
) -> Deposition:
    return Deposition.retrieve(deposition_id, token, base_url)


def upload_file(
        deposition_id: str, path_to_file: str, token: Optional[str] = None
) -> BucketFile:
    deposition: Deposition = retrieve(deposition_id)
    bucket_url = deposition.get_bucket()
    if token is None:
        token = os.getenv("ZENODO_TOKEN")
    path = Path(path_to_file)
    header = {"Authorization": f"Bearer {token}"}
    with open(path_to_file, "rb") as fp:
        r = requests.put(
            f"{bucket_url}/{path.name}",
            data=fp,
            headers=header,
        )
    r.raise_for_status()
    return BucketFile.parse_obj(r.json())


def update_metadata(
        deposition_id: str,
        metadata: Metadata,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
) -> Deposition:
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


def delete_remote(
        deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
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

    response.raise_for_status()
    return response


def publish(
        deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
) -> Deposition:
    if token is None:
        token = os.getenv("ZENODO_TOKEN")
    if base_url is None:
        base_url = os.getenv("ZENODO_URL")
    header = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{base_url}/api/deposit/depositions/{deposition_id}/actions/publish",
        headers=header,
    )

    response.raise_for_status()
    return Deposition.parse_obj(response.json())


def new_version(
        deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
) -> Deposition:
    if token is None:
        token = os.getenv("ZENODO_TOKEN", token)
    if base_url is None:
        base_url = os.getenv("ZENODO_URL")
    header = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{base_url}/api/deposit/depositions/{deposition_id}/actions/newversion",
        headers=header,
    )

    response.raise_for_status()
    deposition: Deposition = Deposition.parse_obj(response.json())
    return deposition


def search(
        query: Optional[str] = None,
        status: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[str] = None,
        size: Optional[int] = None,
        all_versions: Optional[bool] = None,
        token: Optional[str] = None,
) -> list[Deposition]:

    if token is None:
        token = os.getenv("ZENODO_TOKEN")

    base_url = os.getenv("ZENODO_URL")
    header = {"Authorization": f"Bearer {token}"}
    params: dict = {}
    if query is not None:
        params["q"] = query
    if status is not None:
        params["status"] = status
    if sort is not None:
        params["sort"] = sort
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if all_versions:
        params["all_versions"] = "true"
    response = requests.get(
        f"{base_url}/api/deposit/depositions", headers=header, params=params
    )

    response.raise_for_status()
    return [Deposition.parse_obj(x) for x in response.json()]
