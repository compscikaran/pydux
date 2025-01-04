from abc import ABC, abstractmethod
from typing import Callable
from pydux.pydux.api.Action import Action
from pydux.pydux.api.State import State


class Store(ABC):

    @abstractmethod
    def get_state(self) -> State:
        pass

    @abstractmethod
    def dispatch(self, action: Action) -> None:
        pass

    @abstractmethod
    def subscribe(self, consumer: Callable[[State], None]) -> None:
        pass

    @abstractmethod
    def replace_reducer(self, reducer: Callable[[Action, State], State]) -> None:
        pass

    @abstractmethod
    def forwards(self):
        pass

    @abstractmethod
    def backwards(self):
        pass