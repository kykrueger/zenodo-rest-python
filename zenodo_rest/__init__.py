"""zenodo_rest - A python wrapper of Zenodo's REST API for python and the command line."""
from .cli import depositions
from .depositions import actions
from . import entities

__version__ = "0.0.0"
__author__ = "Kyle Krueger <NA>"
__all__: list[str] = []
