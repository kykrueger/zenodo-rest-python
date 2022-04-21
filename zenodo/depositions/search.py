import os
from typing import Optional

import requests

from zenodo.entities import Deposition


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
