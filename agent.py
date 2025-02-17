'''Agent Class definition using Deep Q Learning and e-greedy approach
(exploration vs exploitation)'''

import random
from collections import deque, Counter
import hashlib
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import param


class Snake_Agent():
    '''agent class'''
    def __init__(self, discount: float = 0.9):
        '''init function'''
        # discount factor between 0.9 and 0.99 as per standard implementation
        # and remain constant throughout training
        self._discount: float = discount
        self._session: int = 0
        self._total_session: int = 1
        self._curr_session: int = 0
        self._steps: int = 0
        self._speed: int = 1
        self._random_float: float = random.random()
        self._e: float = param.DEFAULT_E
        # state of training at set interval to show at GUI
        self._training: int = 0
        # state of transferring weights to target network to show at GUI
        self._transfer_weight: int = 0
        # dontlearn state
        self._dontlearn: bool = False
        # initialise 2 MLP network (main and target). One is for training,
        # the other to generate Q target. To prevent chasing a changing
        # objective. Warm_start means training continue from previous weight
        # and learning state, if not it starts from scratch again. As per
        # chatgpt use either adam or sgd because gradient based Liblinear
        # doesnt work, i didn't verify.
        self._main_network: MLPRegressor = MLPRegressor(
            hidden_layer_sizes=(10), warm_start=True,
            max_iter=1000, solver="sgd",
            random_state=param.RANDOM_STATE)
        self._target_network: MLPRegressor = MLPRegressor(
            hidden_layer_sizes=(10),
            random_state=param.RANDOM_STATE)
        # one hot encode action for input into network
        self._action: list = self._one_hot_encode_action()
        # replay buffer would have [[state], action, reward, terminal bool,
        # [next_state]] state
        self._replay_buffer: list[list] = []
        # attribute for loop circuit breaker
        self._recent_states: deque = deque(maxlen=100)
        self._state_counter: Counter = Counter()

    @property
    def session(self) -> int:
        '''getter for session'''
        return self._session

    @property
    def steps(self) -> int:
        '''getter for steps'''
        return self._steps

    @steps.setter
    def steps(self, count: int) -> None:
        '''setter for steps'''
        self._steps += count

    @property
    def transfer_weight(self) -> int:
        '''getter for transfer weight'''
        return self._transfer_weight

    @property
    def training(self) -> int:
        '''getter for training'''
        return self._training

    @property
    def dontlearn(self) -> bool:
        '''getter for dontlearn'''
        return self._dontlearn

    @dontlearn.setter
    def dontlearn(self, state: bool) -> None:
        '''setter for dontlearn'''
        self._dontlearn = state

    @property
    def e(self) -> float:
        '''getter for epsilon'''
        return self._e

    @e.setter
    def e(self, e) -> None:
        '''setter for epsilon'''
        self._e = e

    @property
    def random_float(self) -> float:
        '''getter for random float'''
        return self._random_float

    @property
    def replay_buffer(self) -> list:
        '''getter for replay buffer'''
        return self._replay_buffer

    @replay_buffer.setter
    def replay_buffer(self, value: list) -> None:
        '''setter for replay buffer'''
        self._replay_buffer = value

    @property
    def total_session(self) -> int:
        '''getter for total session'''
        return self._total_session

    @total_session.setter
    def total_session(self, value) -> None:
        '''setter for total_session'''
        self._total_session = value

    @property
    def curr_session(self) -> int:
        '''getter for current session'''
        return self._curr_session

    @curr_session.setter
    def curr_session(self, value) -> None:
        '''setter for current_session'''
        self._curr_session = value

    def add_session(self, count: int) -> None:
        '''add session manually for initial state'''
        self._session += count
        self._curr_session += count

    def _decay_e(self) -> None:
        '''LINEAR decay algo'''
        self._e = max(param.DEFAULT_E * (1 - (
            self.curr_session / self._total_session)
        ), param.MIN_E)

    def _one_hot_encode_action(self) -> list:
        '''return array of one hot encoded action'''
        encoder = OneHotEncoder(sparse_output=False)
        return encoder.fit_transform(
            [[param.Action.UP.value],
             [param.Action.DOWN.value],
             [param.Action.LEFT.value],
             [param.Action.RIGHT.value]
             ])

    def _choose_action(self, info: list) -> int:
        '''returns an action based on exploration/exploitation
        and store info in replay buffer'''
        action: int = 0
        state: list = 0
        # initial state when new game is initiated
        # and initial state with length 1 is given
        initial: bool = True if len(info) == 1 else False
        if initial is True:
            state = info[0]
        else:
            state = info[3]
        # exploration vs exploitation
        self._random_float = random.random()
        if self._random_float < self._e:
            # if exploration choose random action integer
            action = random.randint(list(param.Action)[0].value,
                                    len(param.Action) - 1)
        else:
            # if exploitation, predict a list of 4 Q_target values for
            # each action and choose the max
            action = self._max_q_value(state)
        if self._dontlearn is False:
            # append latest state to end of replay buffer
            # without action encoded input
            self._replay_buffer.append([state.copy()])
            if initial is False:
                # append action encoded input and other info to previous state
                # in replay buffer
                self._replay_buffer[(len(self._replay_buffer)
                                    - 2)].extend(info)
                self._replay_buffer[(len(self._replay_buffer)
                                    - 2)][0].extend(
                                        self._action[info[0]])
                # if fatal is True, amend previous session state
                if info[2] is True:
                    self._decay_e()
                    self._replay_buffer[len(self._replay_buffer)
                                        - 2][4] = []
        return action

    def _max_q_value(self, state: list) -> float:
        '''function to calculate max_q_value for all actions'''
        # extend states with all actions
        state_action: list = [state.copy() for _ in range(len(param.Action))]
        for i, state in enumerate(state_action):
            state.extend(self._action[i])
        q_target: list = [self._target_network.predict([state])
                          for state in state_action]
        # If not training, ie full exploitation, need mechanism
        # to break out of loop due to sparse rewards in larger maps
        # training has exploration so can break out if needed. Can't
        # train 100% to be able to break out of loop
        if self._dontlearn is True and\
           self._is_looping(state.copy()) is True:
            # sort by indices based on largest to smallest q_target value
            sorted_indices = sorted(
                range(len(q_target)), key=lambda i: q_target[i], reverse=True
                )
            # pick second largest value INDEX
            print("loop breakout")
            return sorted_indices[1]
        return q_target.index(max(q_target))

    def _hash_state(self, state: list):
        """Create a unique hash of the snake's state."""
        state_str = f"{state}"
        # Compact 128-bit hash
        return hashlib.md5(state_str.encode()).hexdigest()

    def _is_looping(self, state: list):
        state = self._hash_state(state)
        # Update state frequency
        self._state_counter[state] += 1
        self._recent_states.append(state)
        # Remove oldest state when deque is full
        if len(self._recent_states) == self._recent_states.maxlen:
            oldest_state = self._recent_states[0]
            self._state_counter[oldest_state] -= 1
            if self._state_counter[oldest_state] == 0:
                del self._state_counter[oldest_state]  # Clean up memory
        # Check if state occurs more than threshold
        return self._state_counter[state] > param.MAX_LOOP

    def _train(self) -> None:
        '''training methodology'''
        # 1) pop past experiences if exceed threshold
        if len(self._replay_buffer) > param.REPLAY_SIZE:
            del self._replay_buffer[0]
        # 2) get random sample from replay buffer and fit them.
        if self._steps % param.FREQ == 0 and\
           len(self._replay_buffer) > param.MAX_BATCH_HUNDRED:
            random_sample = random.sample(
                self._replay_buffer[:-1],
                min(len(self._replay_buffer[:-1]), param.MAX_BATCH_HUNDRED)
                )
            # x = input states(distance for each action and
            # one hot encode action)
            x = [state[0] for state in random_sample]
            # y = reward + future reward
            y = [(state[2] + ((self._discount * self._max_q_value(state[4]))
                              if len(state[4]) != 0 else 0))
                 for state in random_sample]
            self._main_network.fit(x, y)
            self._training += 1
        # 3) transfer coefficients and weights to target network
        if self._steps > 1 and self._steps % param.UPDATE_NETWORK == 0:
            self._target_network.coefs_ = [
                np.copy(w) for w in self._main_network.coefs_]
            self._target_network.intercepts_ = [
                np.copy(b) for b in self._main_network.intercepts_]
            self._transfer_weight += 1

    def action(self, info: list) -> int:
        '''outputs an action based on info passed by environment
        and append info in replay buffer for training'''
        # if brand new agent instance (check for coefs_ attribute)
        # set up initial weights for target network
        # with initial inputs and first action and 0 result.
        # Step required so can start generating Q target values
        # although model is untrained
        if hasattr(self._target_network, 'coefs_') is False:
            input_state: list = info[0].copy()
            input_state.extend(self._action[0])
            self._target_network.fit([input_state], [0])
        action: int = self._choose_action(info)
        # if dontlearn is false, 1) train
        # 2) increment permanent step count by 1 for agent for training
        # metrics.
        if self._dontlearn is False:
            self._train()
            self._steps += 1
        return action
