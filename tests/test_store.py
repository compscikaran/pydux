import pytest

from pydux.api.State import State
from pydux.api.Action import Action
from pydux.main.PyDuxStore import PyDuxStore


class UserProfile(State):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __str__(self):
        return f'UserProfile[name={self.name},email={self.email}]'


@pytest.fixture
def my_store():
    initial_state = UserProfile('Karan Gupta', 'karan@hello.com')

    def reducer(action: Action, state: UserProfile)-> UserProfile:
        print('inside reducer')
        print(action.payload_type)
        match action.payload_type:
            case 'SET_EMAIL':
                state.email = action.payload
                print('inside case')
                print(state)
                return state
            case 'SET_NAME':
                state.name = action.payload
                return state
            case default:
                raise KeyError('Action type not supported')

    my_store = PyDuxStore(initial_state=initial_state, reducer=reducer)
    return my_store


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
        return state

    my_store.replace_reducer(do_nothing)

    current_name = my_store.get_state().name
    new_name = 'Sandeep Rajwar'
    action = Action('SET_NAME', new_name)

    my_store.subscribe(lambda x: print(x))
    print(my_store.get_state())
    my_store.dispatch(action)
    assert my_store.get_state().name == current_name