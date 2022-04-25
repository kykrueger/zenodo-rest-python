from .entities.deposition import Deposition


class NoDraftFound(Exception):
    def __init__(self, deposition: Deposition):
        self.deposition: Deposition = deposition

    def __str__(self):
        return f"No drafts were found for the deposition with id: {self.deposition.id} " \
                "make sure that a new version of the deposition exists."
