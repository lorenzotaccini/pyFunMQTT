from abc import ABC, abstractmethod
from typing import Any


class Service(ABC):

    @abstractmethod
    def serve(self, data: Any) -> Any:
        ...


class Split(Service):
    def serve(self, data: str):
        print(list(data))


class Merge(Service):
    def serve(self, data: Any):
        print(data)
