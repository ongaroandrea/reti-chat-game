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

    """ Stampo tutte le informazioni del giocatore """        
    def showInfo(self):
        print ("Nome: ", self.name)
        print ("Ruolo: ", self.role)
        print ("Punteggio: ", self.score)
        print ("Risposte Esatte: ", self.rightAnswers)
    
    """ Restituisco il nome del giocatore """
    def get_name(self):
        return self.name
    
    """ Restituisco il ruolo del giocatore """
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
            return "Citizen"
    
    """ Restituisco il punteggio attuale del giocatore """
    def get_score(self):
        return self.score
    
    """ Restituisco il numero di risposte esatte date"""
    def get_right_answers(self):
        return self.rightAnswers

    """ Restituisco lo stato del giocatore"""    
    def get_status(self):
        return self.status
    
    """ Imposto lo stato del giocatore """
    def set_status(self, status):
        self.status = status
    
    """ Aggiungo il punteggio passato in input al punteggio attuale """
    def add_score(self,val):
        self.score += val
    
    """ Rimuovo il punteggio passato in input al punteggio attuale """
    def remove_score(self,val):
        self.score -= val
    
    """ Incremento di uno le risposte date correttamente """
    def increment_right_answer(self):
        self.rightAnswers += 1
    

