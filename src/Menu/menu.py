# -*- coding: utf-8 -*-
"""
Created on Wed May 12 09:25:30 2021

@author: andre
"""

import random

class Menu:

    def __init__ (self,wrong_choice = None):
        self.wrong_choice = wrong_choice

    def get_wrong_choice(self):
        return self.wrong_choice

    def generate_menu(self):
        self.wrong_choice = random.randint(1,3)
        
    