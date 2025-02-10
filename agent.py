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
        # the other to generate Q target. To prevent chasing a changing objective.
        self._main_network: MLPRegressor = MLPRegressor(hidden_layer_sizes=(10), warm_start=True,
                                             random_state=param.RANDOM_STATE)
        self._target_network: MLPRegressor = MLPRegressor(**self._main_network.get_params())
        # one hot encode action for input into network
        self._action: list = self._one_hot_encode_action()
        self._replay_buffer: list = []

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

    def _one_hot_encode_action(self) -> list:
        '''return array of one hot encoded action'''
        encoder = OneHotEncoder(sparse_output=False)
        return encoder.fit_transform([[[param.Action.UP.value],
                                [param.Action.DOWN.value],
                                [param.Action.LEFT.value],
                                [param.Action.RIGHT.value]
                                ]])

    def choose_action(self, info: list) -> int:
        '''outputs an action based on info passed by environment'''
        # exploration vs exploitation
        if random.random() < self._e:
            return random.randint(list(param.Action)[0].value,
                                  len(param.Action) - 1)
        else:
            # initial state when game is initiated (no prev state)
            if len(info) == 1:
                # set up initial weights for target network if session = 0 in
                # agent with initial inputs and first action and 0 result.
                # Step required so can start generating Q target values
                # although model is untrained
                input: list = info[0].append(self._action[0])
                if self._session == 0:
                    self._target_network.fit(input, [0])
                # predict a list of 4 Q_target values for each action
                q_target: list = [self._target_network.predict(
                    info[0].append(*self._action[action.value]))
                                  for action in list(param.Action)]
                # append info to replay buffer
                self._replay_buffer.append(info[1])
                return q_target.index(max(q_target))
            # subsequent states after action is made
            else:
                q_target: list = [self._target_network.predict(
                    info[3].append(*self._action[action.value]))
                                  for action in list(param.Action)]
                # append new info to new replay buffer
                # and previous replay buffer
                self._replay_buffer.append(info[3])
                self._replay_buffer[
                    (len(self._replay_buffer) - 2)].extend(info)
                return q_target.index(max(q_target))






