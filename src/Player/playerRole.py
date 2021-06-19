# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:11:28 2021

@author: Gruppo Carboni - Ongaro

"""

from enum import Enum

class PlayerRole(Enum) :
    SHERIFF = 0
    OUTLAW = 1
    RENEGADE = 2
    DEPUTY_SHERIFF = 3
    CITIZEN = 4