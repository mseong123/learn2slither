'''Agent Class definition using Deep Q Learning and e-greedy approach(exploration vs exploitation)'''

import random
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import param

class Agent():
    '''agent class'''
    def __init__(self, discount: float = 0.9,
                 decay_scale: float = 0.1):
        '''init function'''
        # discount factor between 0.9 and 0.99 as per standard implementation
        # and remain constant throughout training
        self._discount: float = discount
        self._session: int = 1
        self._steps: int = 0
        # use inverse time decay for e greedy algo. Decay scale measures
        # how fast e decays.
        self._decay_scale: int = decay_scale
        self._e: float = 1
        # initialise 2 MLP network (main and target). One is for training,
        # the other to generate Q target. To prevent chasing a changing 
        # objective.
        self._main_network: MLPRegressor = MLPRegressor(
            hidden_layer_sizes=(10), warm_start=True,
            random_state=param.RANDOM_STATE)
        self._target_network: MLPRegressor = MLPRegressor(
            hidden_layer_sizes=(10),
            random_state=param.RANDOM_STATE)
        # one hot encode action for input into network
        self._action: list = self._one_hot_encode_action()
        # replay buffer would have [[state], action, reward, terminal bool,
        # [next_state]] state
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
        return encoder.fit_transform(
            [[[param.Action.UP.value],
              [param.Action.DOWN.value],
              [param.Action.LEFT.value],
              [param.Action.RIGHT.value]
              ]])

    def _choose_action(self, info: list) -> int:
        '''returns an action based on exploration/exploitation
        and store info in replay buffer'''
        action: int = 0
        # initial state when game is initiated (no prev state)
        initial: bool = True if len(info) == 1 else False
        # exploration vs exploitation
        if random.random() < self._e:
            # if exploration choose random action integer
            action = random.randint(list(param.Action)[0].value,
                                    len(param.Action) - 1)
        else:
            # if exploitation, predict a list of 4 Q_target values for
            # each action and choose the max
            if initial is True:
                action = self._max_q_value(info[0])
                self._replay_buffer.append([info[0]])
            else:
                action = self._max_q_value(info[3]) 
                self._replay_buffer.append([info[3]])
                self._replay_buffer[(len(self._replay_buffer)
                                     - 2)].extend(info)
                if info[2] is True:
                    self._session += 1
        return action

    def _max_q_value(self, state: list) -> float:
        '''function to calculate max_q_value for all actions'''
        q_target: list = [self._target_network.predict(
                           state.append(*self._action[action.value]))
                           for action in list(param.Action)]
        return q_target.index(max(q_target))

    def _train_one(self):
        '''training methodology for < 10 session'''
        # 1) pop past experiences if exceed threshold
        if len(self._replay_buffer > param.REPLAY_SIZE_ONE):
            del self._replay_buffer[0]
        # 2) train every step for session < 10
        # x = input state (list)
        x = [info[0] for info in self._replay_buffer]
        # y = reward + future reward
        y = [(info[1] + (self._discount * self._max_q_value(info[3])))
             for info in self._replay_buffer]
        self._main_network.fit(x, y)
        # 3) transfer coefficients and weights to target network
        if self._steps % param.UPDATE_ONE == 0:
            self._target_network.coefs_ = [
                np.copy(w) for w in self._main_network.coefs_]
            self._target_network.intercepts_ = [
                np.copy(b) for b in self._main_network.intercepts_]


    def _train_ten(self):
        '''training methodology for < 100 session'''
        # 1) pop past experiences if exceed threshold
        if len(self._replay_buffer > param.REPLAY_SIZE_TEN):
            del self._replay_buffer[0]
        # 2) training at interval for session < 100
        # x = input state (list)
        if self._steps % param.FREQ_TEN == 0 and\
            len(self._replay_buffer) > param.MAX_BATCH_TEN:
            x = [info[0] for info in random.sample(self._replay_buffer,
                                                   param.MAX_BATCH_TEN)]
            # y = reward + future reward
            y = [(info[1] + (self._discount * self._max_q_value(info[3])))
                for info in random.sample(self._replay_buffer,
                                          param.MAX_BATCH_TEN)]
            self._main_network.fit(x, y)
        # 3) transfer coefficients and weights to target network
        if self._steps % param.UPDATE_TEN == 0:
            self._target_network.coefs_ = [
                np.copy(w) for w in self._main_network.coefs_]
            self._target_network.intercepts_ = [
                np.copy(b) for b in self._main_network.intercepts_] 


    def _train_hundred(self):
        '''training methodology for >= 100 session'''
        # 1) pop past experiences if exceed threshold
        if len(self._replay_buffer > param.REPLAY_SIZE_HUNDRED):
            del self._replay_buffer[0]
        # 2) training at interval for session >= 100
        # x = input state (list)
        if self._steps % param.FREQ_HUNDRED == 0 and\
            len(self._replay_buffer) > param.MAX_BATCH_HUNDRED:
            x = [info[0] for info in random.sample(self._replay_buffer,
                                                   param.MAX_BATCH_HUNDRED)]
            # y = reward + future reward
            y = [(info[1] + (self._discount * self._max_q_value(info[3])))
                for info in random.sample(self._replay_buffer,
                                          param.MAX_BATCH_HUNDRED)]
            self._main_network.fit(x, y)
        # 3) transfer coefficients and weights to target network
        if self._steps % param.UPDATE_HUNDRED == 0:
            self._target_network.coefs_ = [
                np.copy(w) for w in self._main_network.coefs_]
            self._target_network.intercepts_ = [
                np.copy(b) for b in self._main_network.intercepts_] 

    def _train(self) -> None:
        '''batch sample training from replay buffer. Training methodology
        changes incrementally based on total no. of sessions run by model
        (1, 10, 100) based on subject pdf'''
        if self._session < 10:
            self._train_one()
        elif self._session < 100:
            self._train_ten()
        else:
            self._train_hundred()
           

    def action(self, info: list) -> int:
        '''outputs an action based on info passed by environment
        and append info in replay buffer for training'''
        # set up initial weights for target network if session = 0 in
        # agent with initial inputs and first action and 0 result.
        # Step required so can start generating Q target values
        # although model is untrained
        input_state: list = info[0].append(self._action[0])
        if self._session == 0:
            self._target_network.fit(input_state, [0])
        action: int = self._choose_action(info)
        self._train()
        # increment permanent session count by 1 for agent for training
        # metrics
        self._steps += 1
        return action






