'''Agent Class definition using Deep Q Learning and e-greedy approach(exploration vs exploitation)'''

import random
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder
import param

class Agent():
    '''agent class'''
    def __init__(self, discount: float = 0.9,
                 decay_scale: float = 0.1):
        '''init function'''
        # discount factor between 0.9 and 0.99 as per standard implementation
        # and remain constant throughout training
        self._discount: float = discount
        self._session: int = 0
        # use inverse time decay for e greedy algo. Decay scale measures
        # how fast e decays.
        self._decay_scale: int = decay_scale
        self._e: float = 1
        # initialise 2 MLP network (main and target). One is for training,
        # the other to generate Q Target. To prevent chasing a changing objective.
        main_NN: MLPRegressor = MLPRegressor(hidden_layer_sizes=(10), warm_start=True,
                                             random_state=param.RANDOM_STATE)
        target_NN: MLPRegressor = MLPRegressor(**main_NN.get_params())
        one_hot_encode_action: list = one_hot_encode_action()

    @property
    def session(self) -> int:
        '''getter for session'''
        return self._session

    @session.setter
    def session(self, count: int) -> None:
        '''setter for session'''
        self._session += count

    def _decay_e(self) -> None:
        '''inverse time decay algo to calculate e'''
        self._e = self._e / (1 + (self._decay_scale * self._session))

    def _one_hot_encode(self) -> list:
        '''return array of one hot encoded directions'''
        encoder = OneHotEncoder(sparse_output=False)
        return encoder.fit_transform([[[param.Direction.UP.value],
                                [param.Direction.DOWN.value],
                                [param.Direction.LEFT.value],
                                [param.Direction.RIGHT.value]
                                ]])

    def choose_action(self, info: list) -> int:
        '''outputs an action based on state info passed by environment'''
        if random.random() < self._e:
            return random.randint(list(param.Direction)[0].value,
                                  len(param.Direction) - 1)
        else:





