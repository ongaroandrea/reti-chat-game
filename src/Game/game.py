# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:17:36 2021

@author: Gruppo Carboni - Ongaro
"""
from Game.gameStatus import GameStatus
from Player.player import Player
from Player.playerStatus import PlayerStatus
from Player.playerRole import PlayerRole
from Questions.question import Question
from Menu.menu import Menu

class Game:

    def __init__(self, gameStatus=GameStatus.NOT_STARTED, playerList=[],
                 queue = [], currentPlayer=None, turn=0, question=Question(), 
                 menu=Menu(), round_number=1):

        self.playerList = playerList
        self.queue = queue
        self.gameStatus = gameStatus
        self.currentPlayer = currentPlayer
        self.turn = turn                    # num giocatore che deve giocare
        self.question = question
        self.menu = menu
        self.round_number = round_number    # contatore turni totali

    """ Imposti lo stato del giocatore """
    def set_status(self, status):
        self.gameStatus = status

    """ Ottieni lo stato del giocator """
    def get_status(self):
        return self.gameStatus
    
    """ Ottieni la lista di tutti i giocatori"""
    def get_players(self):
        return self.playerList

    """ Ottengo il giocatore corrente"""
    def get_current_player(self):
        return self.currentPlayer

    """ Controlla che il nome del giocatore passato rispetti le regole """
    def check_name_player(self, name):
        #Controllo nella lista dei giocatori attivi
        for player in self.playerList:
            if player.get_name() == name:
                return True
        
        #Controllo nella lista dei giocatori nella sala d'attesa
        for player in self.queue:
            if player.get_name() == name:
                return True
        return name == None or name == "{start}" and name == "{quit}"

    """ Controlla se il giocatore è nella lista d'attesa """
    def check_queue_players(self,name):
        for player in self.queue:
            if player.get_name() == name:
                return True
        return False
    
    """ Restituisce un giocatore a partire da un nome dato in input """ 
    def get_player(self, name):
        for player in self.playerList:
            if player.get_name() == name:
                return player
        
        for player in self.queue:
            if player.get_name() == name:
                return player
        return None

    """ Controlla che il giocatore sia pronto""" 
    def check_player_ready(self, name):
        return self.get_player(name).get_status() == PlayerStatus.READY

    """ Imposto il gioco come partito, il giocatore corrente e 
        leggo le domande sulla tecnologia """
    def start_game(self):
        self.gameStatus = GameStatus.STARTED
        self.currentPlayer = self.playerList[0]
        self.question.read_question_by_filter("tecnologia")

    """ Controlla che tutti i giocatori siano pronti
        Se sono tutti pronti viene cambiato lo stato dei giocatori e del gioco """
    def check_all_players_ready(self):
        if len(self.playerList) == 1:
            self.gameStatus = GameStatus.NOT_STARTED  #non si può giocare da soli
            return

        for player in self.playerList:
            if player.get_status() == PlayerStatus.NOT_READY:
                self.gameStatus = GameStatus.NOT_STARTED  #i giocatori non sono tutti pronti
                return
            
        self.gameStatus = GameStatus.STARTED
        for player in self.playerList:
            player.set_status(PlayerStatus.PLAYING)

    """ Aggiunta di un giocatore alla lista dei giocatori """ 
    def add_player_to_game_list(self, name):
        self.playerList.append(Player(name, PlayerRole(len(self.playerList) % 4)))

    """ Imposto lo stato del giocatore come non partecipante"""
    def add_player_to_queue(self,name):
        self.queue.append(Player(name, PlayerRole( (len(self.playerList) + len(self.queue)) % 4)))
        
    """ Imposto lo stato del giocatore come pronto""" 
    def set_player_ready(self, name):
        self.get_player(name).set_status(PlayerStatus.READY)
        self.check_all_players_ready()

    """ Rimuovo il giocatore in input """ 
    def remove_player(self, player):
        print("Removing %s" %player.get_name())
        if player in self.queue:
            self.queue.remove(player)
        else:
            self.playerList.remove(player)
    
    """ Imposto lo stato del giocatore come Dead """ 
    def kill_player(self, player):
        player.set_status(PlayerStatus.DEAD)
        print("%s died" %player.get_name())

    """ Passo al giocatore successivo """ 
    def next_player(self):
        if self.turn + 1 == len(self.playerList):  # sono alla fine del giro, devo riiniziarlo
            self.turn = -1
        self.turn += 1  # passo al prossimo giocatore
        while self.playerList[self.turn].get_status() == PlayerStatus.DEAD:
            self.turn += 1  # se un giocatore è morto passo a quello dopo
        self.round_number += 1  # incremento il numero di round totali
        self.gameStatus = GameStatus.STARTED  # riinizio il ciclo di domande
        self.currentPlayer = self.playerList[self.turn]
    
    """ Generazione Menu e controllo risposta del giocatore """ 
    def answer_menu(self, answer):
        self.menu.generate_menu()
        return self.menu.get_wrong_choice() != int(answer)

    """ Genero e restituisco la domanda generata """  
    def get_question(self):
        self.question.generate_question()
        return self.question.get_question()

    """ Controllo la risposta dell'utente""" 
    def answer_question(self, answer):
        return self.question.get_answer() == answer

    """ Aggiungo punti al giocatore corrente """ 
    def add_points(self):
        self.get_current_player().add_score(self.round_number * 100)
        self.get_current_player().increment_right_answer()

    """ Rimuovo i punti al giocatore corrente""" 
    def remove_points(self):
        self.get_current_player().remove_score(100)

    """ Controllo che il gioco possa proseguire o meno""" 
    def check_end(self):
        playersLeft = 0
        for player in self.playerList:
            if player.get_status() == PlayerStatus.PLAYING:
                playersLeft += 1
        print("PLAYERS LEFT: %i" % playersLeft)
        if playersLeft == 1:
            self.gameStatus = GameStatus.ENDED
            return True
        return False

    """  Reimposto lo stato dei giocatori e del gioca allo stato iniziale""" 
    def reset_all(self):
        for player in self.playerList:
            player.set_status(PlayerStatus.NOT_READY)
        self.gameStatus = GameStatus.NOT_STARTED

    """ Ottengo la classifica dei giocatori ordinata a seconda dello stato dei giocatori e del loro punteggio""" 
    def get_rank(self): 
        self.playerList.sort(key=lambda p: (p.get_status() != PlayerStatus.DEAD, p.get_score()), reverse=True)        
        return self.playerList
    
    """ Aggiungo rimasti in sala d'attesa alla lista dei giocatori attuali e cancello la sala d'attesa"""
    def active_queue_players(self):
        for pl in self.queue:
            self.playerList.append(pl)
        
        self.queue.clear()
        