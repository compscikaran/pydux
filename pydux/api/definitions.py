from typing import Callable
from pydux.api.action import Action
from pydux.api.state import T
from pydux.api.store import Store

Consumer = Callable[[T], None]

Reducer = Callable[[Action, T], T]

Middleware = Callable[[Store, Consumer, Action], None]