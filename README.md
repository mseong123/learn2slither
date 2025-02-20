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
          
The above equation shows that the Q value comprises of current reward (provided by the environment) + delayed rewards. This is exemplification of sequential decision making where agent makes a series of decision over time and they impact each others states and rewards. Learned Q values from interacting with the environment through the reward mechanism is propagated through all the states in the second part of the equation above. A well trained agent in theory can forgo immediate rewards for future rewards. Ie don't take a food to stay alive for longer.




In the snake game, my agent's view is limited to 4 direction from it's head, hence I encoded my state to be [dis to wall, dist to good food dist to bad food, dist to tail] for each of the 4 directions and one hot encoded the direction of the snake hence I would have an array of 20 elements for each state. 

![Q_Learning](https://github.com/mseong123/learn2slither/blob/main/images/Q_learning.png)

*Figure 1: Q-Learning*
