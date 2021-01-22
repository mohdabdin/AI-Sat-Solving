# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 21:04:14 2021

@author: gamma
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential(
    [
        layers.Dense(2, activation="relu", name="layer1"),
        layers.Dense(2, activation="relu", name="layer1"),
        layers.Dense(4, name="layer3"),
    ]
)

x = tf.Tensor(["(", "1", "-2", "4", ")(", "-1", "2", "-3", ")(", "-2", "3", "-4", ")"], shape=(13,), dtype=str)