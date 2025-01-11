from typing import Callable
from pydux.api.action import Action
from pydux.api.state import T
import copy


def action_creator(action_type: str, payload: str | dict | T) -> Action: return Action(action_type, payload)


def combine_reducer(*reducers: Callable[[Action, T], T]) -> Callable[[Action, T], T]:

    def combined_func(action: Action, state: T) -> T:
        new_state = copy.copy(state)
        for reducer in reducers:
            new_state = reducer(action, new_state)
        return new_state

    return combined_func