# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:17:36 2021

@author: andre
"""
from Game.gameStatus import GameStatus
from Player.player import Player
from Player.playerStatus import PlayerStatus

class Game:
    
    def __init__ (self,gameStatus = GameStatus.NOT_STARTED, playerList = []):
        self.playerList = playerList
        self.gameStatus = gameStatus


    def get_status(self):
        return self.gameStatus

    def get_players(self):
        return self.playerList
    
    def get_player_by_index(self, index):
        return self.playerList[index]
    
    def start_game(self):
        if len(self.playerList) == 1 :
            self.gameStatus = GameStatus.NOT_STARTED #non si può giocare da soli
            return False
        
        if self.gameStatus == GameStatus.STARTED:
            self.gameStatus = GameStatus.NOT_STARTED #impossibile far partire un'altra partita quando è già partita una
            return False
        
        for player in self.playerList:
            if player.getStatus == PlayerStatus.NOT_READY:
                self.gameStatus = GameStatus.NOT_STARTED #i giocatori non sono tutti pronti
                return  False
            
        self.gameStatus = GameStatus.STARTED #Non ci sono stati intoppi, il gioco è partito
        return True
        #parte il timer
        #currentPlayer = Primo
        #Mostrare i primi tre menu
        #catturare la scelta dell'utente
        #a seconda della scelta cancellare il giocatore o mostrare la domanda
        #Mostrare la domanda e avviare un timer
        #Se non risponde entro il timer - risposta sbagliata
        #Se risponde male - risposta sbagliata
        #Se risponde bene - Aumentare il punteggio (Il punteggio dato è tanto più grande a seconda del livello in cui siamo)
        #Cos'è un livello? Ogni volta che si torna al primo posto si aggiunge un livello
        #Si passa all'altra persona
        
    def addPlayerToGameList(self,name):
        self.playerList.append(Player(name,"role"))
        
    def setPlayerReady(self, index):
        self.get_player_by_index.setStatus = PlayerStatus.READY
    
    def removePlayer(self,player):
        if self.get_player_by_index(1) == player:
            #cambiare chi è il primo
            print("smo")
        self.playerList.remove(player)

#Probabilmente inutil
if __name__ == "__main__":
    game = Game()
        