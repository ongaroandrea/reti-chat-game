# -*- coding: utf-8 -*-
"""
Created on Wed May 12 12:19:12 2021

@author: andre
"""

import json 

class Question:
    
    def __init__ (self,question = "", answer = "",info = "",listQuestion = []):
         self.question = question
         self.answer = answer
         self.info = info
         self.listQuestion = listQuestion
    
    def get_question(self):
        return self.question
    
    def get_answer(self) : 
        return self.answer

    def get_info(self) :
        return self.info
    
    def read_question_by_filter(self,filtro):
        f = open('../../assets/questions/domande.json', )
        data = json.load(f)
        self.listQuestion = data[filtro]
        
    def generate_question(self, counter):
        question = self.listQuestion[counter];
        self.question = question['domanda']
        self.answer = question['risposta']
        self.info = question['info']