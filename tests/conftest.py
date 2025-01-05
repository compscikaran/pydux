import pytest
from pydux.api.State import State
from pydux.api.Action import Action
from pydux.main.PyDuxStore import PyDuxStore

class BaseData:
    INITIAL_NAME = 'Karan Gupta'
    INITIAL_EMAIL = 'karan@hello.com'


class UserProfile(State):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __str__(self):
        return f'UserProfile[name={self.name},email={self.email}]'


@pytest.fixture(autouse=True)
def my_store():
    initial_state = UserProfile(BaseData.INITIAL_NAME, BaseData.INITIAL_EMAIL)

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