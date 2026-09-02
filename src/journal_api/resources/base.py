from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Client

class BaseResource:
    def __init__(self, client: "Client"):
        self.client = client