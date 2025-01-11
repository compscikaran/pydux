from typing import Callable, Optional
from typing_extensions import override
from pydux.api.action import Action
from pydux.api.definitions import Reducer, Middleware, Consumer
from pydux.api.store import Store
from pydux.main.time_travel import TimeTravel
from pydux.api.state import T
import copy


class PyDuxStore(Store):

    def __init__(self, initial_state: T, reducer: Reducer, middleware: Optional[Middleware] | None = None):
        self.state = initial_state
        self.reducer = reducer
        self.middleware = middleware
        self.listeners = []
        self.time_travel = TimeTravel()
        self.time_travel.record_change(Action(TimeTravel.INITIAL_STATE, initial_state))


    @override
    def get_state(self) -> T:
        return self.state


    @override
    def dispatch(self, action: Action) -> None:
        if self.middleware is not None:
            self.middleware(self, self._dispatch, action)
        else:
            self._dispatch(action)


    def _dispatch(self, action: Action) -> None:
        if action.payload_type == TimeTravel.INITIAL_STATE:
            return
        new_state = self.reducer(action, copy.deepcopy(self.state))
        self.state = new_state
        self.time_travel.record_change(action)
        self.notify_subscribers()


    def notify_subscribers(self) -> None:
        [listener(self.state) for listener in self.listeners]


    @override
    def subscribe(self, consumer: Consumer) -> None:
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

