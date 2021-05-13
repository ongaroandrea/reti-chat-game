# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:17:36 2021

@author: andre
"""
from Game.gameStatus import GameStatus
from Player.player import Player
from Player.playerStatus import PlayerStatus
from Questions.question import Question
from Menu.menu import Menu
import threading

class Game:
    
    def __init__ (self,gameStatus = GameStatus.NOT_STARTED, playerList = [], 
                  currentPlayer = None,turn = 0, question = Question(), menu = Menu(), counter = 0) :
        
        self.playerList = playerList
        self.gameStatus = gameStatus
        self.currentPlayer = currentPlayer
        self.turn = turn
        self.question = question
        self.menu = menu
        self.counter = counter
    
    def set_status(self, status):
        self.gameStatus = status

    def get_status(self):
        return self.gameStatus

    def get_players(self):
        return self.playerList
    
    def get_current_player(self):
        return self.currentPlayer

    def get_player_by_index(self, index):
        return self.playerList[index]
    
    def check_name_player(self, name):
        return self.get_player(name) != None
    
    def get_player(self,name):
        for player in self.playerList:
            if player.get_name() == name:
                return player
        return None

    def check_player_status(self, name):
        player = self.get_player(name)
        return player.get_status() == PlayerStatus.READY
    
    
    def start_timer(self, time): # una nuova classe timer?
        timer = threading.Timer(time,self.check_all_players_ready()) # cambiare funzione
        timer.start()
        
    def start_game(self):  
        #self.start_timer(2.0)
        self.gameStatus = GameStatus.STARTED
        self.currentPlayer = self.playerList[0]
        print("CURRENT PLAYA:" + self.playerList[0].get_name())
    
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
        
    def addPlayerToGameList(self,name):
        self.playerList.append(Player(name,"role"))
        
    def setPlayerReady(self, name):
        player = self.get_player(name)
        player.set_status(PlayerStatus.READY)
        self.check_all_players_ready()
        
    def removePlayer(self,player):
        self.playerList.remove(player)
    
    def next_player(self):
        print( "LUNGHEZZA %i",len(self.playerList))
        print( "CONT %i",self.counter)
        if len(self.playerList) == self.counter - 1:
            self.counter = -1
            self.turn += 1
        self.counter += 1
        self.gameStatus = GameStatus.MENU_PHASE
        return self.playerList[0] # da modificare, ma non ho capito perchè qui il playerList è grandezza 1 mentre dovrebbe essere due con due giocatori
    
    def answer_menu(self,answer):
        # controllare che sia compresa tra 1 e 3 e che sia un numero
        self.menu.generate_menu()
        return self.menu.get_correct_choice() == int(answer)
            
    def get_question(self):
        self.question.read_question_by_filter("tecnologia")
        self.question.generate_question(1)
        return self.question.get_question()
    
    def answer_question(self,answer):
        return self.question.get_answer() == answer

        