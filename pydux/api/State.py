from dataclasses import dataclass


@dataclass
class State:
    pass


from typing import TypeVar
T = TypeVar('T', bound='State')