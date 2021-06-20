# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:27:43 2021

@author: Gruppo Carboni - Ongaro

"""
from enum import Enum

class GameStatus(Enum) :
    NOT_STARTED = 0
    STARTED = 1
    MENU_PHASE = 2
    QUESTION_PHASE = 3
    ENDED = 4