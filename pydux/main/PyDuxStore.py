from typing import Callable
from typing_extensions import override
from pydux.pydux.api.Action import Action
from pydux.pydux.api.State import State
from pydux.pydux.api.Store import Store
from pydux.pydux.main.TimeTravel import TimeTravel
import copy


class PyDuxStore(Store):

    def __init__(self, initial_state: State, reducer: Callable[[Action, State], State]):
        self.state = initial_state
        self.reducer = reducer
        self.listeners = []
        self.time_travel = TimeTravel()
        self.time_travel.record_change(Action.model_validate(
            {'type': TimeTravel.INITIAL_STATE, 'payload': initial_state}))

    def get_state(self) -> State:
        return self.state

    @override
    def dispatch(self, action: dict) -> None:
        action_instance = Action.model_validate(action)
        new_state = self.reducer(action_instance, copy.deepcopy(self.state))
        if new_state != self.state:
            self.state = new_state
            self.time_travel.record_change(action_instance)
            self.notify_subscribers()

    def notify_subscribers(self) -> None:
        [listener(self.state) for listener in self.listeners]

    def subscribe(self, consumer: Callable[[State], None]) -> None:
        self.listeners.append(consumer)

    def replace_reducer(self, reducer: Callable[[Action, State], State]) -> None:
        self.reducer = reducer

    def forwards(self):
        self.time_travel.go_forwards()
        action_to_apply = self.time_travel.get_latest_action()
        self.dispatch(action_to_apply)

    def backwards(self):
        self.time_travel.go_backwards()
        self.state = self.time_travel.get_initial_state()
        history = self.time_travel.get_action_history()
        for action in history:
            action_instance = Action.model_validate(action)
            self.state = self.reducer(action_instance, copy.deepcopy(self.state))
        self.notify_subscribers()

