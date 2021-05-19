#!/usr/bin/env python3
"""
Created on Sat May  8 19:17:36 2021

@author: Gruppo Carboni - Ongaro

"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading 
from Game.game import Game
from Game.gameStatus import GameStatus
import time as tm 

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accetta_connessioni_in_entrata():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        
        if game.get_status() == GameStatus.STARTED:
             client.send(bytes("Il gioco è attualmente in esecuzione - RIPROVA PIU' TARDI", "utf8"))
        else: 
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            if len(game.get_players()) > 0:
                client.send(bytes("Sono già presenti i seguenti giocatori: \n", "utf8"))
                for player in game.get_players():
                    client.send(bytes(player.get_name() + " \n", "utf8"))
            # ci serviamo di un dizionario per registrare i client
            indirizzi[client] = client_address
            #diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=gestice_client, args=(client,)).start()
        

"""La funzione seguente gestisce la connessione di un singolo client."""
def gestice_client(client):  # Prende il socket del client come argomento della funzione.
       
    nome = client.recv(BUFSIZ).decode("utf8") #--------------------------------SCELTA NOME
    while game.check_name_player(nome) or nome == "{start}":
        client.send(bytes('Il nome %s è già stato utilizzato o è incompatibile. Scegline un altro' %nome, "utf8"))
        nome = client.recv(BUFSIZ).decode("utf8")
    
    game.addPlayerToGameList(nome) #-------------------------------------------AGGIUNTA GIOCATORE

    #BENVENUTO
    client.send(bytes('Benvenuto %s! Se vuoi lasciare la Chat' % nome, "utf8"))
    client.send(bytes('Clicca il pulsante Pronto per dichiararti pronto \n', "utf8"))
    client.send(bytes('{quit} per uscire dal gioco', "utf8"))
    
    broadcast(bytes("%s si è unito alla chat!" % nome, "utf8"))
    
    clients[client] = nome
    global timerGame
    global timerQuestion
    global gameStatus
    global currentPlayer
    
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ)
        gameStatus = game.get_status()
        
        #----------------------------------------------------------------------COMANDI
        if msg == QUIT: #------------------------------------------------------QUIT
            client.send(bytes("Si è scelto di uscire", "utf8"))
            client.close()
            broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
            del clients[client]
            break
        elif msg == START and gameStatus != GameStatus.NOT_STARTED: #----------START SE GIA COMINCIATO
            client.send(bytes("Gioco già cominciato!", "utf8"))
            #Non deve proseguire
        elif msg == START and game.check_player_ready(nome): #----------------START SE GIA PRONTO
            client.send(bytes('Ti sei già dichiarato pronto', "utf8"))
            #Non deve proseguire
        elif msg == START and gameStatus != GameStatus.STARTED: #--------------START
            game.setPlayerReady(nome)
            broadcast(bytes("Il giocatore %s è pronto" % nome, "utf8"))
            if game.get_status() == GameStatus.STARTED:
                broadcast(bytes("\nTutti pronti, si parte!", "utf8"))
                game.start_game()
                timerGame = start_countdown(50, GameStatus.ENDED, True, None, end_function)
        else: #----------------------------------------------------------------BROADCAST MESSAGGIO (NO COMANDO)
            broadcast(msg, nome+": ")
        
        currentPlayer = ""
        gameStatus = game.get_status()
        if gameStatus != GameStatus.NOT_STARTED and gameStatus != GameStatus.ENDED: # se il gioco è partito
            currentPlayer = game.get_current_player().get_name()
            
            if gameStatus == GameStatus.STARTED: #-----------------------------GIOCO INIZIATO, TESTO SCELTA PORTA
                broadcast(bytes("\nTurno di: %s. " % currentPlayer, "utf8"))
                broadcast(bytes("\nScegli una porta tra 1, 2 e 3.", "utf8"))
                game.set_status(GameStatus.MENU_PHASE)
            else:
                if currentPlayer == nome: #check giocatore
                    if gameStatus == GameStatus.MENU_PHASE: #------------------PORTA SCELTA
                        if msg.decode().isnumeric():#-------------------------CHECK INSERIMENTO NUMERICO
                            if int(msg) == 1 or int(msg) == 2 or int(msg) == 3:
                                if game.answer_menu(msg): #------------------------PORTA CON DOMANDA
                                    broadcast(bytes(game.get_question(), "utf8"))
                                    game.set_status(GameStatus.QUESTION_PHASE)
                                    gameStatus = GameStatus.QUESTION_PHASE
                                    timerQuestion = start_countdown(5, GameStatus.MENU_PHASE, False, GameStatus.QUESTION_PHASE, stop_time_answer)
                                else: #--------------------------------------------PORTA BOMBA
                                    broadcast(bytes("%s è entrato nella porta sbagliata!." %nome, "utf8"))
                                    game.next_player()
                                    game.removePlayer(game.get_player(currentPlayer)) 
                                    if game.check_end():
                                        
                                        game.set_status(GameStatus.ENDED)
                                        gameStatus = GameStatus.ENDED
                                    else:
                                        game.set_status(GameStatus.STARTED)
                                        broadcast(bytes("%s se ne va!." %nome, "utf8"))
                                        currentPlayer = game.get_current_player().get_name()
                                        broadcast(bytes("\nTurno di: %s. " % currentPlayer, "utf8"))
                                        broadcast(bytes("\nScegli una porta tra 1, 2 e 3.", "utf8"))
                                        game.set_status(GameStatus.MENU_PHASE)
                                        gameStatus = GameStatus.MENU_PHASE
                            else:
                                 client.send(bytes("Inserimento Errato, Scegli una porta tra 1, 2 , 3", "utf8"))
                        else:
                            client.send(bytes("Inserimento Errato, Scegli una porta tra 1, 2 , 3", "utf8"))
                            
                    elif gameStatus == GameStatus.QUESTION_PHASE:
                        answer = msg.decode()
                        if game.answer_question(answer):
                            game.add_points()
                            broadcast(bytes("Risposta esatta, punteggio aumentato!", "utf8"))
                        else:
                            broadcast(bytes("Risposta errata!", "utf8"))
                        game.next_player()
                        currentPlayer = game.get_current_player().get_name()
                        broadcast(bytes("\nTurno di: %s. " % currentPlayer, "utf8"))
                        broadcast(bytes("\nScegli una porta tra 1, 2 e 3.", "utf8"))
                        game.set_status(GameStatus.MENU_PHASE)
                else:
                    client.send(bytes("Non è il tuo turno", "utf8"))
    
""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)

def countdown(duration, quitStatus, alwaysDo, doStatus, function):
    thisQuestionPlayer = currentPlayer
    
    #il countdown si ferma quando finisce i secondi o quando il gioco arriva allo stato definito
    while duration > 0 and gameStatus != quitStatus: 
        tm.sleep(1)
        duration -= 1
        print(duration)
    #timer ended - eseguo la funzione specificata quando il flag alwaysDo è true
    #oppure quando sono in doStatus ed il giocatore è lo stesso
    if alwaysDo: 
        function()
    else:
        if gameStatus == doStatus and thisQuestionPlayer == currentPlayer:
            function()
    
    
def start_countdown(duration, quitStatus, alwaysDo, doStatus, function):
    countdown_thread = threading.Thread(target=countdown, args=(duration, quitStatus, alwaysDo, doStatus, function,))
    countdown_thread.daemon = True #rendo il thread deamon, alla chiusura del server morirà
    countdown_thread.start()
    return countdown_thread
    
def print_winner():
   for p in game.get_players():
       print(p.get_name())

def stop_time_answer():
    broadcast(bytes("Tempo Scaduto per rispondere", "utf8"))
    game.next_player()
    currentPlayer = game.get_current_player().get_name()
    broadcast(bytes("\nTurno di: %s. " % currentPlayer, "utf8"))
    broadcast(bytes("\nScegli una porta tra 1, 2 e 3.", "utf8"))
    game.set_status(GameStatus.MENU_PHASE)
    gameStatus = GameStatus.MENU_PHASE
    
def end_function():
    rank = game.get_players() # getrank ma è vuoto adesso
    winner = game.get_players()[0]
    broadcast(bytes("%s Ha vinto." %winner.get_name(), "utf8"))
    tm.sleep(1)
    game.set_status(GameStatus.ENDED)
    ##stampa classifica
    broadcast(bytes("\nGioco Terminato. Classifica:", "utf8"))
    i = 0
    for player in rank:
        i += 1
        broadcast(bytes("\n{}°: {}, {}\n".format(i, player.get_name(), player.get_score()), "utf8"))
        tm.sleep(1)
    #reset gioco
    game.reset_all()
    broadcast(bytes("Premi Pronto per giocare ad una nuova partita!", "utf8"))

clients = {}
indirizzi = {}
HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
game = Game()
START = bytes("{start}", "utf8")
QUIT = bytes("{quit}", "utf8")
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
