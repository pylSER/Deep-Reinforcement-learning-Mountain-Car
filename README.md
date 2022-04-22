<!--
title:DQN Mountain Car Deep Reinforcement learning OpenAI gym
categories: DQN Mountain Car Deep Reinforcement learning OpenAI gym
description: DQN Mountain Car Deep Reinforcement learning OpenAI gym
keywords: DQN Mountain Car Deep Reinforcement learning OpenAI gym

<meta name='DQN Mountain Car' content='Deep Reinforcement learning OpenAI gym quick'>  -->

I found a new generation audio edit website: www.voicefloat.com


# A SUPER QUICK way to train Mountain Car using DQN

Reinforcement Learning DQN - using OpenAI gym Mountain Car

- Keras
- gym

### The training will be done in at most 6 minutes! (After about 300 episodes the network will converge



[![DQN](http://img.youtube.com/vi/4kTxLr2NjYY/0.jpg)](http://www.youtube.com/watch?v=4kTxLr2NjYY "DQN")



The program in the video is running in macOS(Macbook Air) , and it only took 4.1 minutes to finish training. No GPU used.  

## Using GPU

You can use codes:

````python
import tensorflow as tf
import keras
config = tf.ConfigProto( device_count = {'GPU': 2 , 'CPU': 1} ) 
sess = tf.Session(config=config) 
keras.backend.set_session(sess)
````

and change the trainFromBuffer function to **Boost**

````
#self.trainFromBuffer()
self.trainFromBuffer_Boost()
````

I used a workstation to run GPU version. It took about 2mins to finish training.

## How to test

run `testMountainCar.py`

change the file path in 

````
#load the network
model=models.load_model('your model filepath')
````

Then you can see how the car plays the game.













