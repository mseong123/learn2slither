# learn2slither | 42KL
### Gameplay
<div style="display: flex;">
  <img src="https://github.com/mseong123/learn2slither/blob/main/images/lobby.png" alt="Lobby" style="width: 45%; margin-right: 50px;"/>
  <img src="https://github.com/mseong123/learn2slither/blob/main/images/game.png" alt="Gameplay" style="width: 45%;"/>
</div>

<br/>
<hr/>

### Introduction

This project aims to introduce the concept of Reinforcement Learning which is a machine learning algorithm that allows an agent to learn through numerous trial and error using a reward/penalty mechanism to find an optimum solution to a problem set. Q(uality) learning aims to learn a Q-value for each action at every state and the Q-value gets updated when the agent goes through the state again multiple times through an exploration/exploitation mechanism. The purpose of a Q-value is for to evaluate the 'quality' of a certain action at a state. 

### Q-function

The Q function is in the form of Bellman equation:

          Q(s) = Reward + Discount_rate( max Q(s+1) )
          
The above equation shows that the Q value comprises of current reward (provided by the environment) + delayed/future rewards. This is exemplification of sequential decision making where agent makes a series of decision over time and they impact each others states and rewards. Learned Q values from interacting with the environment through the reward mechanism is propagated through all the states in the second part of the equation above. A well trained agent in theory can forgo immediate rewards for future rewards. Ie don't take a food to stay alive for longer.

### Simple illustration of how Q learning works and how Q value future value propagates using the Bellman Equation:

#### First Session

1. ![grid1](https://github.com/mseong123/learn2slither/blob/main/images/grid1.png)
    - For this illustration purpose:
    - Food reward: +20, Empty spaces penalty: -1 (to penalize agent for taking unneccesary steps), discount rate: 1 (for ease of illustration calculation)
3.  ![grid2](https://github.com/mseong123/learn2slither/blob/main/images/grid2.png)
    - Agent chooses to move right for illustration purpose. Based on Bellman's equation, current reward is -1 and future value is 0 (since it hasn't moved to any other grids/states yet and doesn't know the rewards). Hence Q value is -1 for this grid.
3.  ![grid3](https://github.com/mseong123/learn2slither/blob/main/images/grid3.png)
    - Agent moves right again. Since it doesn't know future rewards, Q value is -1 for this grid
4.  ![grid4](https://github.com/mseong123/learn2slither/blob/main/images/grid4.png)
    - Once it moves right, it receives 20 reward (assume the game ends at this state hence no future value). Q value = 20

#### Second Session

1.  ![grid5](https://github.com/mseong123/learn2slither/blob/main/images/grid5.png)
    - Agent starts again from initial position and moves right. Q value = -1 (current reward) + 1 (-1) = -2
2.  ![grid6](https://github.com/mseong123/learn2slither/blob/main/images/grid6.png)
    - Agent moves right. Q value = -1 (current reward) + 1 (20) = 19

#### Third Session

1.  ![grid5](https://github.com/mseong123/learn2slither/blob/main/images/grid6.png)
    - Agent starts again from initial position and moves right. Q value = -1 (current reward) + 1 (19) = 18

Hence from the above, we can see that if the agent travels through the grid/states multiple times, it will learn that turning right (with Q value of 18) will get it to a food and if it train over multiple cycles, it will find an optimum route to maximise it's length and not die at the same time.

![Q_Learning](https://github.com/mseong123/learn2slither/blob/main/images/Q_learning.png)

*Figure showing how the environment interacts with the agent*

### Deep Q Learning

In the snake game, the agent's view is limited to 4 direction from it's head, hence I encoded my state to be [dis to wall, dist to good food dist to bad food, dist to tail] for each of the 4 directions and one hot encoded the direction of the snake hence I would have an array of 20 elements for each state. The distances are normalized relation to grid size hence their values are between 0 and 1. This ensures that the agent can generalize well and work on board of any grid size. Since the values in my state is a continuous variable, neural network is best suitable to approximate the Q value instead of using a Q table as the state space is large (potentially infinite) and the agent wouldn't be able to visit the states enough times to update the Q values. 

## **PERSONAL KEY FINDINGS FROM PROJECT** 

1. The encoding of states are important to ensure that the network learns properly. Ie if you multiply distance with rewards, it might end up confusing the the signals provided to the agent.
2. Modularity matters, environment should be detached from agent. Agent should only receive state information and associate them with rewards. The agent shouldn't know other environment specific information like ie walls, red apples. This allows the agent to be used even when the environment variable changes and multiple agents can also be used within the same game.
3. There is no single right approach to train the agent. Through multiple trial and errors I found that:
   - training initially using a smaller grid size (ie 7) allows the snake to encounter more rewards and hence reinforce the signals of these +ve behaviors. If I run my model directly on a grid size of 10 and since there's only 2 green apples spawned each time, my model will be highly unstable since low chance to encounter a positive reward.
   - More training ≠ better performance. I found that an agent trained on a grid size of 7 for 2500 episodes and then trained on a grid size of 10 for 40000 episodes performs worse than an agent trained 2500 episodes on a grid size of 5,7,8,9,10 (totalling 12500 episodes). Key findings is train on an initial set of parameters first to stabilize training and observe improved performance then gradually expand the training on other parameters..
4. Reward structure is highly important. Too low rewards, agent doesn't learn enough since signal is weak. Too high rewards, will produce unexpected behaviors (skew the results). Ie To encourage snake to move around, I initially gave +1 reward when moving to an empty space, however the accumulation of Q values moving in empty spaces overwhelmed the signal of food rewards resulting in agent moving around randomly without picking up food.
5. Exploration is important to prevent overfitting and able to navigate well in a sparse reward environment (ie 15 x 15 grid with only 2 food at each time)

<br/>

### Run model
```
python snake.py <arguments>
```
#### Valid arguments
 - --help => show list of available arguments





