# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:11:28 2021

@author: andre
"""

from enum import Enum

class PlayerRole(Enum) :
    SHERIFF = 0
    OUTLAW = 1
    RENEGADE = 2
    DEPUTY_SHERIFF = 3
    CITIZEN = 4
    
    #2People -> SHERIFF AND OUTLAW
    
    #3People -> SHERIFF RENEGADE AND OUTLAW
    
    #4People -> SHERIFF DEPUTY_SHERIFF RENEGADE AND OUTLAW
    
    #5People -> SHERIFF DEPUTY_SHERIFF RENEGADE AND 2 OUTLAW
    
    #6People -> SHERIFF 2 DEPUTY_SHERIFF RENEGADE AND 2 OUTLAW
    
    #7People -> SHERIFF 2 DEPUTY_SHERIFF 2 RENEGADE AND 2 OUTLAW
    
    #8People -> SHERIFF 2 DEPUTY_SHERIFF 2 RENEGADE AND 3 OUTLAW