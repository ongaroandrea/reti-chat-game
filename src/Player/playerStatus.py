# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:00:49 2021

@author: andre
"""

from enum import Enum

class PlayerStatus(Enum) :
    NOT_READY = 0
    READY = 1
    PLAYING = 2
    DEAD = 3