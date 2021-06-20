# -*- coding: utf-8 -*-
"""
Created on Wed May 12 09:25:30 2021

@author: Gruppo Carboni - Ongaro

"""

import random

class Menu:

    def __init__ (self,wrong_choice = None):
        self.wrong_choice = wrong_choice

    """ Ottengo la porta errata del menu """
    def get_wrong_choice(self):
        return self.wrong_choice

    """ Genero la porta errata tra le tre disponibili """
    def generate_menu(self):
        self.wrong_choice = random.randint(1,3)
        
    