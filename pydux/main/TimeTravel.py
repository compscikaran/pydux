from argparse import Action
from pydux.api.State import State


class TimeTravel:

    SNAPSHOT_THRESHOLD = 10
    INITIAL_STATE = 'INITIAL_STATE'

    def __init__(self):
        self.actions: list[Action] = []
        self.snapshot = None
        self.index = 0

    def record_change(self, action: Action) -> None:
        self.actions.append(action)
        self.index += 1

    def get_initial_state(self) -> State:
        return self.actions[0].payload

    def get_action_history(self) -> list[Action]:
        return self.actions[1:self.index]

    def get_latest_action(self) -> Action:
        return self.actions[len(self.actions) - 1] if len(self.actions) > 0 else None

    def go_forwards(self):
        self.index += 1

    def go_backwards(self):
        self.index -= 1