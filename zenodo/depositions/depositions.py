import json
import os
from typing import Optional

import click
from requests import Response

from zenodo.entities import Deposition, Metadata

from .search import search


@click.group()
def depositions():
    pass


@depositions.command()
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
def create(
    metadata: Optional[str] = None,
    metadata_file: Optional[str] = None,
    prereserve_doi: Optional[bool] = None,
):

    metadata_parsed: Metadata = Metadata()
    if isinstance(metadata, str):
        metadata_parsed = Metadata.parse_raw(metadata)
    elif isinstance(metadata, Metadata):
        metadata_parsed = metadata

    if metadata_file is not None:
        metadata_parsed = Metadata.parse_file(metadata_file)

    deposition: Deposition = Deposition.create(metadata_parsed, prereserve_doi)
    if not os.getenv("ZENODO_SILENT"):
        json_response = deposition.json(exclude_none=True, indent=4)
        click.echo(json_response)


@depositions.command()
@click.argument("deposition-id", type=click.INT)
def retrieve(deposition_id: int):
    """Retrieve deposition by ID from server.

    DEPOSITION-ID is the id of the deposition to be fetched
    """
    deposition: Deposition = Deposition.retrieve(deposition_id)
    if not os.getenv("ZENODO_SILENT"):
        json_response = deposition.json(exclude_none=True, indent=4)
        click.echo(json_response)


@depositions.command("list")
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
def search_depositions(
    query: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    page: Optional[str] = None,
    size: Optional[int] = None,
    all_versions: bool = None,
):
    result: list[Deposition]
    result = search(query, status, sort, page, size, all_versions)
    if not os.getenv("ZENODO_SILENT"):
        for x in result:
            click.echo(x.json(exclude_none=True, indent=2))


@depositions.command()
@click.argument("deposition_id", type=click.INT)
@click.argument(
    "metadata_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def update(
    deposition_id: int,
    metadata_file: str,
):
    """Update metadata for a not yet published deposition

    DEPOSITION_ID the id of the deposition to be updated

    METADATA_FILE the path to a metadata json file to be used as input
    """

    metadata = Metadata.parse_file(metadata_file)

    deposition: Deposition = Deposition.static_update_metadata(deposition_id, metadata)
    if not os.getenv("ZENODO_SILENT"):
        json_response = deposition.json(exclude_none=True, indent=4)
        click.echo(json_response)


@depositions.command()
@click.argument("deposition_id", type=click.INT)
def delete(
    deposition_id: int,
):
    """Delete a not yet published deposition

    DEPOSITION_ID the id of the deposition to be deleted
    """

    deposition: Response = Deposition.static_delete_remote(deposition_id)
    if not os.getenv("ZENODO_SILENT"):
        json_response = deposition.json(exclude_none=True, indent=4)
        click.echo(json_response)


@depositions.command()
@click.argument("deposition_id", type=click.INT)
@click.argument(
    "file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def upload_file(
    deposition_id: int,
    file: str,
):
    """Upload a file to the bucket of a not yet published deposition

    DEPOSITION_ID the id of the deposition to upload to

    FILE the path to a file to be uploaded
    """
    deposition: Deposition = Deposition.retrieve(deposition_id)
    response = deposition.upload_file(file)
    if not os.getenv("ZENODO_SILENT"):
        json_response = json.dumps(response.json(), indent=4)
        click.echo(json_response)
