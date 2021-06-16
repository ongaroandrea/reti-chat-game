# -*- coding: utf-8 -*-
"""
Created on Sat May  8 13:20:20 2021

@author: Gruppo Carboni - Ongaro
"""
from Player.playerStatus import PlayerStatus 
from Player.playerRole import PlayerRole

class Player :
    
    def __init__ (self, name, role,score = 0,rightAnswers = 0,status = PlayerStatus.NOT_READY):
         
        self.name = name
        self.role = role 
        self.score= score
        self.rightAnswers = rightAnswers
        self.status = status
        
    def showInfo(self):
        print ("Nome: ", self.name)
        print ("Ruolo: ", self.role)
        print ("Punteggio: ", self.score)
        print ("Risposte Esatte: ", self.rightAnswers)
    
    def get_name(self):
        return self.name
    
    def get_role(self):
        if self.role == PlayerRole.SHERIFF:
            return "Sheriff"
        elif self.role == PlayerRole.OUTLAW:
            return "Outlaw"
        elif self.role == PlayerRole.RENEGADE:
            return "Renegade"
        elif self.role == PlayerRole.DEPUTY_SHERIFF:
            return "Deputy Sheriff"
        else:
            return "Citzen"
    
    def get_score(self):
        return self.score
    
    def get_right_answers(self):
        return self.rightAnswers
    
    def get_status(self):
        return self.status
        
    def set_status(self, status):
        self.status = status
    
    def add_score(self,val):
        self.score += val
        
    def remove_score(self,val):
        self.score -= val
    
    def increment_right_answer(self):
        self.rightAnswers += 1
    

