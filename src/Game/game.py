# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:17:36 2021

@author: andre
"""
from Game.gameStatus import GameStatus
from Player.player import Player
from Player.playerStatus import PlayerStatus
from Questions.question import Questions
from Menu.menu import Menu
import threading
import random

class Game:
    
    def __init__ (self,gameStatus = GameStatus.NOT_STARTED, playerList = [], currentPlayer = None,firstPlayer = None):
        self.playerList = playerList
        self.gameStatus = gameStatus
        self.currentPlayer = currentPlayer
        self.firstPlayer = firstPlayer

    def get_status(self):
        return self.gameStatus

    def get_players(self):
        return self.playerList
    
    def get_current_player(self):
        return self.currentPlayer

    def get_player_by_index(self, index):
        return self.playerList[index]
    
    def check_name_player(self, name):
        if self.get_player(name) != None:
            return True
        return False
    
    def get_player(self,name):
        for player in self.playerList:
            if player.get_name() == name:
                return player
        return None

    def check_player_status(self, name):
        player = self.get_player(name)
        if player.get_status() == PlayerStatus.READY:
            return True
        else:
            return False
    
    
    def start_timer(self, time):
        timer = threading.Timer(time)
        timer.start()
        
        
    def start_game(self):  
        timer = threading.Timer(2.0,self.next_player())
        timer.start()
        self.currentPlayer = self.playerList[0]
        print(self.playerList[0].get_name())

    
    def get_questions(self):
        #Mostrare i primi tre menu
        question1, answer1, info1 = Questions.generate_question()
        question2, answer2, info2 = Questions.generate_q()
        
        menu = [
            (question1, answer1, info1)
            (question2, answer2, info2)
            (None, None, None)
            ]
        random.shuffle(menu)
        
        return menu
        
        
        
        #catturare la scelta dell'utente
        #a seconda della scelta cancellare il giocatore o mostrare la domanda
        #Mostrare la domanda e avviare un timer
        #Se non risponde entro il timer - risposta sbagliata
        #Se risponde male - risposta sbagliata
        #Se risponde bene - Aumentare il punteggio (Il punteggio dato è tanto più grande a seconda del livello in cui siamo)
        #Cos'è un livello? Ogni volta che si torna al primo posto si aggiunge un livello
        #Si passa all'altra persona
        
        #return True
        
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
    
    def check_all_players_ready(self):
        if len(self.playerList) == 1:
            self.gameStatus = GameStatus.NOT_STARTED #non si può giocare da soli
            return False
        
        if self.gameStatus == GameStatus.STARTED:
            #impossibile far partire un'altra partita quando è già partita una ??????
            return False
        
        for player in self.playerList:
            if player.get_status() == PlayerStatus.NOT_READY:
                self.gameStatus = GameStatus.NOT_STARTED #i giocatori non sono tutti pronti
                return  False
        
        self.gameStatus = GameStatus.STARTED
        return True
        
    def stop_game():
        return None
        
    def addPlayerToGameList(self,name):
        self.playerList.append(Player(name,"role"))
        
    def setPlayerReady(self, name):
        player = self.get_player(name)
        player.set_status(PlayerStatus.READY)
        self.check_all_players_ready()
        
    def removePlayer(self,player_name):
        if self.get_player_by_index(0).get_name == player_name:
            self.firstPlayer = self.get_player_by_index(1) #per gestire i turni

        self.playerList.remove(player_name)# non funzion, è sbagliato
    
    def next_player(self):
        print("nextPlayer")
    
    def answer_menu(answer):
        #magari controllare che sia compresa tra 1 e 3
        m = Menu()
        m.generate_menu()
        if m.get_correct_choice() == int(answer):
            return True
        else:
            return False
            
    def answer_game(self,answer):
        return True