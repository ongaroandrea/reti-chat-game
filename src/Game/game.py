# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:17:36 2021

@author: andre
"""
from Game.gameStatus import GameStatus
from Player.player import Player
from Player.playerStatus import PlayerStatus
from Player.playerRole import PlayerRole
from Questions.question import Question
from Menu.menu import Menu
import threading

class Game:
    
    def __init__ (self, gameStatus = GameStatus.NOT_STARTED, playerList = [], 
                  currentPlayer = None,turn = 0, question = Question(), menu = Menu(), round_number = 0) :
        
        self.playerList = playerList
        self.gameStatus = gameStatus
        self.currentPlayer = currentPlayer
        self.turn = turn #num giocatore che deve giocare
        self.question = question
        self.menu = menu
        self.round_number = round_number # contatore turni totali
    
    def set_status(self, status):
        self.gameStatus = status

    def get_status(self):
        return self.gameStatus

    def get_players(self):
        return self.playerList
    
    def get_current_player(self):
        return self.currentPlayer
    
    def check_name_player(self, name): #unused
        return self.get_player(name) != None
    
    def get_player(self,name):
        for player in self.playerList:
            if player.get_name() == name:
                return player
        return None

    def check_player_ready(self, name):
        return self.get_player(name).get_status() == PlayerStatus.READY
        
    def start_game(self):
        self.gameStatus = GameStatus.STARTED
        self.currentPlayer = self.playerList[0]
        self.question.read_question_by_filter("tecnologia")
    
    # Declaring private method
    def _check_all_players_ready(self):
        if len(self.playerList) == 1:
            self.gameStatus = GameStatus.NOT_STARTED #non si può giocare da soli
            return 
        if self.gameStatus == GameStatus.STARTED:
            #impossibile far partire un'altra partita quando è già partita una ??????
            #CONTROLLA QUESTA COSA
            return #False
        
        for player in self.playerList:
            if player.get_status() == PlayerStatus.NOT_READY:
                self.gameStatus = GameStatus.NOT_STARTED #i giocatori non sono tutti pronti
                return 
        # game starts
        self.gameStatus = GameStatus.STARTED
        for player in self.playerList:
            player.set_status(PlayerStatus.PLAYING)
        
    def addPlayerToGameList(self,name):
        self.playerList.append(Player(name, PlayerRole(len(self.playerList) % 4 ) ))
        
    def setPlayerReady(self, name):
        self.get_player(name).set_status(PlayerStatus.READY)
        self._check_all_players_ready()
        
    def removePlayer(self,player):
        player.set_status(PlayerStatus.DEAD)
        #self.turn -= 1 decrementa quando qualcuno muore?
            
    def next_player(self):
        if self.turn + 1 == len(self.playerList): #sono alla fine del giro, devo riiniziarlo
            self.turn = -1
        self.turn += 1 # passo al prossimo giocatore
        while self.playerList[self.turn].get_status() == PlayerStatus.DEAD:
            self.turn +=1 #se un giocatore è morto passo a quello dopo
        self.round_number += 1 # incremento il numero di round totali
        self.gameStatus = GameStatus.STARTED #riinizio il ciclo di domande
        self.currentPlayer = self.playerList[self.turn]
    
    def answer_menu(self,answer):
        self.menu.generate_menu()
        #print("PORTA CON BOMBA: %i" %self.menu.get_wrong_choice())
        return self.menu.get_wrong_choice() != int(answer)
            
    def get_question(self):
        self.question.generate_question()
        return self.question.get_question()
    
    def answer_question(self,answer):
        return self.question.get_answer() == answer

    def add_points(self):
        self.get_current_player().add_score(self.round_number * 100)
        self.get_current_player().increment_right_answer()
    
    def remove_points(self):
        self.get_current_player().remove_score(100)
    
    def check_end(self):
        playersLeft = 0
        for player in self.playerList:
            if player.get_status() == PlayerStatus.PLAYING:
                playersLeft += 1
        print("PLAYERS LEFT: %i" %playersLeft)
        if playersLeft == 1: 
            self.gameStatus = GameStatus.ENDED
            return True
        return False
    
    def check_winner(self):
        winner = ""
        for player in self.get_rank():
            if player.get_status() == PlayerStatus.PLAYING:
                winner = player.get_name()
        self.gameStatus = GameStatus.ENDED
        return winner
    
    def reset_all(self):
        for player in self.playerList:
            player.set_status(PlayerStatus.NOT_READY)
        self.gameStatus = GameStatus.NOT_STARTED
    
    def get_rank(self):
        #Devo ottenere in ordine la lista delle persone che se ne sono andate
        self.playerList.sort(key=lambda p: (p.get_score(), p.get_status() != PlayerStatus.DEAD ) )
                
    def method_t(self):
        for player in self.playerList:
            print(player.get_role())