from pydantic import BaseModel
from pydux.pydux.api.State import State


class Action(BaseModel):
    type: str
    payload: State