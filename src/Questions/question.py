# -*- coding: utf-8 -*-
"""
Created on Wed May 12 12:19:12 2021

@author: Gruppo Carboni - Ongaro
"""

import json 
import random

class Question:
    
    def __init__ (self,question = "", answer = "", 
                  info = "", listQuestion = []) :
         self.question = question
         self.answer = answer
         self.info = info
         self.listQuestion = listQuestion
    
    """ Ottengo la domanda caricata dal file """
    def get_question(self):
        return self.question
    
    """ Ottengo la risposta esatta caricata dal file """
    def get_answer(self): 
        return self.answer

    """ Ottengo informazioni aggiuntive sulla domanda corrente """
    def get_info(self):
        return self.info
    
    """ Ottengo tutte le domande dal file a seconda del filtro impostato """
    def read_question_by_filter(self,filtro):
        f = open('../assets/Questions/domande.json', "rb")
        data = json.load(f, encoding="utf-8")
        self.listQuestion = data[filtro]
     
    """ Imposto tutte le variabili per una domanda ottenuta casualmente 
        dalla lista salvata """
    def generate_question(self):
        question = self.listQuestion[random.randint(0, len(self.listQuestion) - 1)];
        self.question = question['domanda']
        self.answer = question['risposta']
        self.info = question['info']