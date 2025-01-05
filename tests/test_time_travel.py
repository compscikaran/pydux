from pydux.api.Action import Action
from pydux.main.PyDuxStore import PyDuxStore
from tests.conftest import BaseData


def test_can_go_back(my_store: PyDuxStore):
    new_email = 'karan@gmail.com'
    action = Action('SET_EMAIL', new_email)
    my_store.subscribe(lambda x: print(x))
    print(my_store.get_state())
    my_store.dispatch(action)
    my_store.backwards()
    assert my_store.get_state().email == BaseData.INITIAL_EMAIL

def test_can_go_forward(my_store: PyDuxStore):
    new_email = 'karan@gmail.com'
    action = Action('SET_EMAIL', new_email)
    my_store.subscribe(lambda x: print(x))
    print(my_store.get_state())
    my_store.dispatch(action)
    my_store.backwards()
    my_store.forwards()
    assert my_store.get_state().email == new_email
