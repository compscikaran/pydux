from typing import Callable
from typing_extensions import override
from pydux.api.Action import Action
from pydux.api.Store import Store
from pydux.main.TimeTravel import TimeTravel
from pydux.api.State import T
import copy


class PyDuxStore(Store):

    def __init__(self, initial_state: T, reducer: Callable[[Action, T], T]):
        self.state = initial_state
        self.reducer = reducer
        self.listeners = []
        self.time_travel = TimeTravel()
        self.time_travel.record_change(Action(TimeTravel.INITIAL_STATE, initial_state))

    @override
    def get_state(self) -> T:
        return self.state

    @override
    def dispatch(self, action: Action) -> None:
        if action.payload_type == TimeTravel.INITIAL_STATE:
            return
        new_state = self.reducer(action, copy.deepcopy(self.state))
        self.state = new_state
        self.time_travel.record_change(action)
        self.notify_subscribers()

    def notify_subscribers(self) -> None:
        [listener(self.state) for listener in self.listeners]

    @override
    def subscribe(self, consumer: Callable[[T], None]) -> None:
        self.listeners.append(consumer)

    @override
    def replace_reducer(self, reducer: Callable[[Action, T], T]) -> None:
        self.reducer = reducer

    @override
    def forwards(self):
        self.time_travel.go_forwards()
        action_to_apply = self.time_travel.get_latest_action()
        self.dispatch(action_to_apply)

    @override
    def backwards(self):
        self.time_travel.go_backwards()
        self.state = self.time_travel.get_initial_state()
        history = self.time_travel.get_action_history()
        for action in history:
            self.state = self.reducer(action, copy.deepcopy(self.state))
        self.notify_subscribers()

