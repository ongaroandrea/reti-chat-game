# -*- coding: utf-8 -*-
"""
Created on Sat May  8 09:07:36 2021

@author: andre
"""

import json 

f = open('questions/tech.json', )

data = json.load(f)
    
questions = data['questions']
print(questions[1].get('question'))
