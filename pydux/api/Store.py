from abc import ABC, abstractmethod
from typing import Callable
from typing_extensions import Generic
from pydux.api.State import T
from pydux.api.Action import Action


class Store(ABC):

    @abstractmethod
    def get_state(self) -> Generic[T]:
        pass

    @abstractmethod
    def dispatch(self, action: Action) -> None:
        pass

    @abstractmethod
    def subscribe(self, consumer: Callable[[T], None]) -> None:
        pass

    @abstractmethod
    def replace_reducer(self, reducer: Callable[[Action, T], T]) -> None:
        pass

    @abstractmethod
    def forwards(self):
        pass

    @abstractmethod
    def backwards(self):
        pass