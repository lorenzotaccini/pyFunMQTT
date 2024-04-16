from abc import ABC, abstractmethod
from typing import Any


class Service(ABC):
    _registry = {}

    @classmethod
    def registry(cls):
        return cls._registry

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls()

    @abstractmethod
    def serve(self, data: Any) -> Any:
        ...


class Split(Service):
    def serve(self, data: Any):
        pass


class Merge(Service):
    def serve(self, data: Any):
        print(data)
