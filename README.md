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

          Q(s) = Reward + Discount( max Q(s+1)
          
The Q 




In the snake game, my agent's view is limited to 4 direction from it's head, hence I encoded my state to be [dis to wall, dist to good food dist to bad food, dist to tail] for each of the 4 directions and one hot encoded the direction of the snake hence I would have an array of 20 elements for each state. 

![Q_Learning](https://github.com/mseong123/learn2slither/blob/main/images/Q_learning.png)

*Figure 1: Q-Learning*
