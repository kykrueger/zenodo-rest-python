import os
from typing import Optional

import requests

from zenodo_rest.entities.deposition import Deposition
from zenodo_rest.entities.metadata import Metadata


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
