import os

import click
from dotenv import load_dotenv

from zenodo.depositions import depositions

@click.group()
@click.option(
    "--token",
    is_flag=True,
    show_default="ENVVAR: 'ZENODO_TOKEN'",
    help="Request a prompt to provide an authtoken to override ZENODO_TOKEN.",
)
@click.option(
    "--env", "-e",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Pass a path to a .env file to overwrite and add ENVVARS.",
)
def cli(token: str = None, env: str = None):
    if env:
        load_dotenv(dotenv_path=env, override=True)
    if token:
        os.putenv('ZENODO_TOKEN', token)

cli.add_command(depositions)

def main():
    cli()


if __name__ == '__main__':
    main()