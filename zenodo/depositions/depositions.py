import click


from .create import create


@click.group()
def depositions():
    pass


depositions.add_command(create)
