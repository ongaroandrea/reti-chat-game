# -*- coding: utf-8 -*-
"""
Created on Sat May  8 09:07:36 2021

@author: andre
"""

import json 

def read_question_by_filter(filtro):
    f = open('questions/domande.json', )
    data = json.load(f)
    return data[filtro]
    
    
    
    
