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

Hence from the above, we can see that if the agent travels and learns enough it will learn that turning right (with Q value of 18) will get it to a food. 

### Deep Q Learning


In the snake game, my agent's view is limited to 4 direction from it's head, hence I encoded my state to be [dis to wall, dist to good food dist to bad food, dist to tail] for each of the 4 directions and one hot encoded the direction of the snake hence I would have an array of 20 elements for each state. 

![Q_Learning](https://github.com/mseong123/learn2slither/blob/main/images/Q_learning.png)

*Figure 1: Q-Learning*
