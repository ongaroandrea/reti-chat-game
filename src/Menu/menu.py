# -*- coding: utf-8 -*-
"""
Created on Wed May 12 09:25:30 2021

@author: andre
"""

import random

class Menu:

    def __init__ (self,correct_choice = None):
        self.correct_choice = correct_choice

    def get_correct_choice(self):
        return self.correct_choice

    def generate_menu(self):
        self.correct_choice = random.randint(1,3)
        
    