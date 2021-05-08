# -*- coding: utf-8 -*-
"""
Created on Sat May  8 13:20:20 2021

@author: Gruppo Carboni - Ongaro
"""

class Player :
    
    def __init__ (self, name, role,score = 0,rightAnswers = 0 ):
         
        self.name = name
        self.role = role 
        self.score= score
        self.rightAnswers = rightAnswers
     
    def showInfo(self):
         
        print ("Nome: ", self.name)
        print ("Ruolo: ", self.role)
        print ("Punteggio: ", self.score)
        print ("Risposte Esatte: ", self.rightAnswers)
    
    def getName(self):
        return self.name
    
    def getRole(self):
        return self.role
    
    def getScore(self):
        return self.score
    
    def getRightAnswers(self):
        return self.rightAnswers
    
    def addScore(self,val):
        self.score += val
    
    def incrementRightAnswer(self):
        self.rightAnswers += 1
