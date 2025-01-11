from pydux.api.action import Action
from pydux.api.store import Store
from pydux.main.pydux_store import PyDuxStore
from pydux.api.definitions import Consumer

SPECIAL_INPUT = "Tom Marvolo Riddle"
TRANSFORMED_INPUT = "Lord Voldemort"


def store_with_middleware(my_store: PyDuxStore):

    def middleware(store: Store, consumer: Consumer, action: Action) -> None:
        if action.payload_type == 'SET_NAME' and action.payload == SPECIAL_INPUT:
            changed_action = Action(action.payload_type, TRANSFORMED_INPUT)
            consumer(changed_action)
        else:
            consumer(action)

    return PyDuxStore(initial_state=my_store.get_state(), reducer=my_store.reducer, middleware=middleware)

def test_middleware_works(my_store: PyDuxStore):
    new_store = store_with_middleware(my_store)
    action = Action('SET_NAME', SPECIAL_INPUT)
    new_store.subscribe(lambda x: print(x))
    print(my_store.get_state())
    new_store.dispatch(action)
    assert new_store.get_state().name == TRANSFORMED_INPUT