from pydux.api.State import T

class Action:
    def __init__(self, payload_type: str, payload: str | dict | T):
        self.payload_type = payload_type
        self.payload = payload
