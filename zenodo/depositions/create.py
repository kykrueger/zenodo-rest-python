import json
import os
from typing import Optional, Union

import click
import requests
from dotenv import load_dotenv

from zenodo.entities.deposition import Deposition
from zenodo.entities.metadata import Metadata

load_dotenv()


@click.command()
@click.option("--metadata", help="Optional json of metadata for the deposition.")
@click.option(
    "--metadata_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Optional json file of metadata for the deposition.",
)
@click.option(
    "--prereserve-doi",
    is_flag=True,
    help="Prereserve a DOI (not pushed to Datacite until deposition is published).",
)
@click.option("--silent", default=False, help="Don't print any output")
def create(
    metadata: Union[str, Metadata, None] = Metadata(),
    metadata_file: Optional[str] = None,
    prereserve_doi: Optional[bool] = None,
    silent: bool = True,
    token: Optional[str] = None,
):
    if token is None:
        token = os.getenv("ZENODO_TOKEN")

    metadata_parsed: Metadata
    if metadata is None:
        metadata_parsed = Metadata()
    elif isinstance(metadata, str):
        metadata_parsed = Metadata.parse_raw(metadata)
    elif isinstance(metadata, Metadata):
        metadata_parsed = metadata

    if metadata_file is not None:
        metadata_parsed = Metadata.parse_file(metadata_file)

    if prereserve_doi is True:
        metadata_parsed.prereserve_doi = True

    base_url = os.getenv("ZENODO_URL")
    header = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{base_url}/api/deposit/depositions",
        json={"metadata": metadata_parsed.dict(exclude_none=True)},
        headers=header,
    )
    if not silent:
        json_response = json.dumps(response.json(), indent=4)
        click.echo(json_response)

    response.raise_for_status()
    return Deposition.parse_obj(response.json())


if __name__ == "__main__":
    create()
