from pydux.api.Action import Action
from pydux.main.PyDuxStore import PyDuxStore
from tests.conftest import UserProfile, BaseData


def test_can_change_email(my_store: PyDuxStore):
    new_email = 'karan@gmail.com'
    action = Action('SET_EMAIL', new_email)
    my_store.subscribe(lambda x: print(x))
    print(my_store.get_state())
    my_store.dispatch(action)
    assert my_store.get_state().email == new_email

def test_can_change_name(my_store: PyDuxStore):
    new_name = 'Sandeep Rajwar'
    action = Action('SET_NAME', new_name)
    my_store.subscribe(lambda x: print(x))
    print(my_store.get_state())
    my_store.dispatch(action)
    assert my_store.get_state().name == new_name

def test_can_replace_reducer(my_store: PyDuxStore):

    def do_nothing(action: Action, state: UserProfile) -> UserProfile:
        print(action)
        return state

    my_store.replace_reducer(do_nothing)
    my_store.subscribe(lambda x: print(x))
    new_name = 'Sandeep Rajwar'
    action = Action('SET_NAME', new_name)
    print(my_store.get_state())
    my_store.dispatch(action)
    assert my_store.get_state().name == BaseData.INITIAL_NAME