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
            #client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
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

    global matchIndex
    global currentPlayer
    global game
    
    nome = client.recv(BUFSIZ).decode("utf8") #--------------------------------SCELTA NOME
    while game.check_name_player(nome) or nome == "{start}":
        client.send(bytes('Il nome %s è già stato utilizzato o è incompatibile. Scegline un altro' %nome, "utf8"))
        nome = client.recv(BUFSIZ).decode("utf8")
    
    game.addPlayerToGameList(nome) #-------------------------------------------AGGIUNTA GIOCATORE

    #BENVENUTO
    client.send(bytes('Benvenuto %s! Se vuoi lasciare la Chat' % nome, "utf8"))
    client.send('Clicca il pulsante Pronto per dichiararti pronto'.encode())
    client.send('{quit} per uscire dal gioco'.encode())
    
    broadcast("%s si è unito alla chat!" % nome)
    
    clients[client] = nome
    
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        gameStatus = game.get_status()
        
        #----------------------------------------------------------------------COMANDI
        if msg == QUIT: #------------------------------------------------------QUIT
            client.send("Si è scelto di uscire".encode())
            client.close()
            broadcast("%s ha abbandonato la Chat." % nome)
            del clients[client]
            break
        elif msg == START and gameStatus != GameStatus.NOT_STARTED: #----------START SE GIA COMINCIATO
            client.send("Gioco già cominciato!".encode())
            #Non deve proseguire
        elif msg == START and game.check_player_ready(nome): #----------------START SE GIA PRONTO
            client.send('Ti sei già dichiarato pronto'.encode())
            #Non deve proseguire
        elif msg == START and gameStatus != GameStatus.STARTED: #--------------START
            game.setPlayerReady(nome)
            broadcast("Il giocatore %s è pronto" % nome)
            if game.get_status() == GameStatus.STARTED:
                broadcast("\nTutti pronti, si parte!")
                matchIndex += 1
                game.start_game()
                start_countdown(50, GameStatus.ENDED, True, None, end_function)
        else: #----------------------------------------------------------------BROADCAST MESSAGGIO (NO COMANDO)
            broadcast(msg, nome+": ")
        
        currentPlayer = ""
        gameStatus = game.get_status()
        if gameStatus != GameStatus.NOT_STARTED and gameStatus != GameStatus.ENDED: # se il gioco è partito
            currentPlayer = game.get_current_player().get_name()
            
            if gameStatus == GameStatus.STARTED: #-----------------------------GIOCO INIZIATO, TESTO SCELTA PORTA
                broadcast("\nTurno di: %s. " % currentPlayer)
                broadcast("\nScegli una porta tra 1, 2 e 3.")
                game.set_status(GameStatus.MENU_PHASE)
            else:
                if currentPlayer == nome: #check giocatore
                    if gameStatus == GameStatus.MENU_PHASE: #------------------PORTA SCELTA
                        if msg.isnumeric():#-------------------------CHECK INSERIMENTO NUMERICO
                            if int(msg) == 1 or int(msg) == 2 or int(msg) == 3:
                                if game.answer_menu(msg): #------------------------PORTA CON DOMANDA
                                    broadcast(game.get_question())
                                    game.set_status(GameStatus.QUESTION_PHASE)
                                    gameStatus = GameStatus.QUESTION_PHASE
                                    start_countdown(5, GameStatus.MENU_PHASE, False, GameStatus.QUESTION_PHASE, stop_time_answer)
                                else: #--------------------------------------------PORTA BOMBA
                                    broadcast("%s è entrato nella porta sbagliata!." %nome)
                                    game.next_player()
                                    game.removePlayer(game.get_player(currentPlayer)) 
                                    if game.check_end():
                                        game.set_status(GameStatus.ENDED)
                                        gameStatus = GameStatus.ENDED
                                        end_function()
                                    else:
                                        game.set_status(GameStatus.STARTED)
                                        broadcast("%s se ne va!." %nome)
                                        currentPlayer = game.get_current_player().get_name()
                                        broadcast("\nTurno di: %s. " % currentPlayer)
                                        broadcast("\nScegli una porta tra 1, 2 e 3.")
                                        game.set_status(GameStatus.MENU_PHASE)
                                        gameStatus = GameStatus.MENU_PHASE
                            else:
                                 client.send(bytes("Inserimento Errato, Scegli una porta tra 1, 2 , 3", "utf8"))
                        else:
                            client.send(bytes("Inserimento Errato, Scegli una porta tra 1, 2 , 3", "utf8"))
                            
                    elif gameStatus == GameStatus.QUESTION_PHASE:
                        if game.answer_question(msg):
                            game.add_points()
                            broadcast("Risposta esatta, punteggio aumentato!")
                        else:
                            game.remove_points()
                            broadcast("Risposta errata!")
                        game.next_player()
                        currentPlayer = game.get_current_player().get_name()
                        broadcast("\nTurno di: %s. " % currentPlayer)
                        broadcast("Scegli una porta tra 1, 2 e 3.")
                        game.set_status(GameStatus.MENU_PHASE)
                else:
                    client.send(bytes("Non è il tuo turno", "utf8"))
    
""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8") + bytes(msg, "utf8"))

def countdown(duration, quitStatus, alwaysDo, doStatus, function):
    thisCountdownMatchIndex = matchIndex
    thisPlayer = currentPlayer
    #il countdown si ferma quando finisce i secondi o quando il gioco arriva allo stato definito
    while duration > 0 and gameStatus != quitStatus: 
        tm.sleep(1)
        duration -= 1
        #print(duration)
    #timer ended - eseguo la funzione specificata quando il flag alwaysDo è true
    #oppure quando sono in doStatus ed il giocatore è lo stesso
    if alwaysDo and thisCountdownMatchIndex == matchIndex and game.get_status() != GameStatus.ENDED and game.get_status() != GameStatus.NOT_STARTED: 
        function()
    else:
        actualGameStatus = game.get_status()
        #print(currentPlayer)
        #print(thisPlayer)
        if actualGameStatus == doStatus and thisCountdownMatchIndex == matchIndex and thisPlayer == currentPlayer:
            function()
    
    
def start_countdown(duration, quitStatus, alwaysDo, doStatus, function):
    countdown_thread = threading.Thread(target=countdown, args=(duration, quitStatus, alwaysDo, doStatus, function,))
    countdown_thread.daemon = True #rendo il thread deamon, alla chiusura del server morirà
    countdown_thread.start()
    #return countdown_thread

def stop_time_answer():
    broadcast("Tempo Scaduto per rispondere")
    game.remove_points()
    game.next_player()
    currentPlayer = game.get_current_player().get_name()
    broadcast("\nTurno di: %s. " % currentPlayer)
    broadcast("\nScegli una porta tra 1, 2 e 3.")
    game.set_status(GameStatus.MENU_PHASE)
    #gameStatus = GameStatus.MENU_PHASE
    
def end_function():
    rank = game.get_rank() # getrank ma è vuoto adesso
    winner = rank[0]
    broadcast("%s Ha vinto." %winner.get_name())
    tm.sleep(1)
    game.set_status(GameStatus.ENDED)
    ##stampa classifica
    broadcast("\nGioco Terminato. Classifica:", "utf8")
    i = 0
    for player in rank:
        i += 1
        broadcast("\n{}°: {}, {}, {}\n".format(i, player.get_name(), player.get_score(), player.get_status()))
        tm.sleep(1)
    #reset gioco
    game.reset_all()
    broadcast("Premi Pronto per giocare ad una nuova partita!")

clients = {}
indirizzi = {}
HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
game = Game()
START = "{start}"
QUIT = "{quit}"
timerGame = ""
timerQuestion = ""
gameStatus = ""
currentPlayer = ""
matchIndex = 0
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
