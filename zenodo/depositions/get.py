import json
import os
from typing import Optional

import click
import requests
from dotenv import load_dotenv

from zenodo.entities.deposition import Deposition

load_dotenv()


@click.command()
@click.option(
    "--query", "-q", help="Search query (using Elasticsearch query string syntax)."
)
@click.option(
    "--status", help="Filter result based on deposit status (either draft or published)"
)
@click.option(
    "--sort",
    help=(
        "Sort order (bestmatch or mostrecent)."
        "Prefix with minus to change form ascending to descending (e.g. -mostrecent)."
    ),
)
@click.option("--page", help="Page number for pagination")
@click.option("--size", help="Number of results to return per page.")
@click.option(
    "--all-versions",
    help="Show (true or 1) or hide (false or 0) all versions of deposits.",
)
@click.option("--silent", default=False, help="Don't print any output")
@click.option(
    "--token",
    prompt=True,
    prompt_required=False,
    hide_input=True,
    show_default="ENVVAR: 'ZENODO_TOKEN'",
    help="Required when the envvar is not set.",
)
def get(
    query: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    page: Optional[str] = None,
    size: Optional[int] = None,
    all_versions: bool = None,
    silent: bool = True,
    token: Optional[str] = None,
) -> list[Deposition]:
    if token is None:
        token = os.getenv("ZENODO_TOKEN")

    base_url = os.getenv("ZENODO_URL")
    header = {"Authorization": f"Bearer {token}"}
    params: dict = {}
    if query is not None:
        params['q'] = query
    if status is not None:
        params['status'] = status
    if sort is not None:
        params['sort'] = sort
    if all_versions:
        params['all_versions'] = 'true'
    response = requests.get(f"{base_url}/api/deposit/depositions", headers=header, params=params)
    if not silent:
        json_response = json.dumps(response.json(), indent=4)
        click.echo(json_response)

    response.raise_for_status()
    return [Deposition(**x) for x in response.json()]


if __name__ == "__main__":
    get()
