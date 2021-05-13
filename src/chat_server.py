#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from Game.game import Game
from Game.gameStatus import GameStatus

import random

START = bytes("{start}", "utf8")
QUIT = bytes("{quit}", "utf8")

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accetta_connessioni_in_entrata():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        
        if game.get_status() == GameStatus.STARTED:
             client.send(bytes("Il gioco è attualmente in esecuzione - RIPROVA PIU' TARDI", "utf8"))
        else: 
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            # ci serviamo di un dizionario per registrare i client
            indirizzi[client] = client_address
            #diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=gestice_client, args=(client,)).start()
        

"""La funzione seguente gestisce la connessione di un singolo client."""
def gestice_client(client):  # Prende il socket del client come argomento della funzione.
       
    nome = client.recv(BUFSIZ).decode("utf8")
    while game.check_name_player(nome) or nome == "{start}":
        client.send(bytes('Il nome %s è già stato utilizzato o è incompatibile. Scegline un altro' %nome, "utf8"))
        nome = client.recv(BUFSIZ).decode("utf8")
    
    game.addPlayerToGameList(nome)

    client.send(bytes('Benvenuto %s! Se vuoi lasciare la Chat' % nome, "utf8"))
    client.send(bytes('Clicca il pulsante Pronto per dichiararti pronto \n', "utf8"))
    client.send(bytes('{quit} per uscire dal gioco', "utf8"))

    broadcast(bytes("%s si è unito alla chat!" % nome, "utf8"))
    
    clients[client] = nome
    
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ)
        gameStatus = game.get_status()
        
        if msg == QUIT: #------------------------------------------------------QUIT
            client.send(bytes("Si è scelto di uscire", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
            break
        elif msg == START and gameStatus != GameStatus.NOT_STARTED: #----------ALREADY STARTED
            client.send(bytes("Gioco già cominciato!", "utf8"))
        elif msg == START and game.check_player_status(nome): #----------------ALREADY READY
            client.send(bytes('Ti sei già dichiarato pronto', "utf8"))
        elif msg == START and gameStatus != GameStatus.STARTED: #--------------READY
            game.setPlayerReady(nome)
            broadcast(bytes("Il giocatore %s è pronto" % nome, "utf8"))
            
            if game.get_status() == GameStatus.STARTED:
                broadcast(bytes("\nTutti pronti, si parte!", "utf8"))
                game.start_game()
                # dopo questo non stampa il turno, bisogna scrivere qualcosa in chat
        else:
            broadcast(msg, nome+": ")
        
        currentPlayer = ""
        if gameStatus != GameStatus.NOT_STARTED: # se il gioco è partito
            currentPlayer = game.get_current_player().get_name() # ottengo il nome del giocatore attuale
            
            if gameStatus == GameStatus.STARTED: #-----------------------------GIOCO INIZIATO, SCEGLI PORTA
                broadcast(bytes("\nTurno di: %s. " % currentPlayer, "utf8"))
                broadcast(bytes("\nScegli una porta tra 1, 2 e 3.", "utf8"))
                game.set_status(GameStatus.MENU_PHASE)
                
            if currentPlayer == nome: #se scrive il giocatore attuale
                if gameStatus == GameStatus.MENU_PHASE: #----------------------PORTA SCELTA, SCEGLI RISPOSTA ALLA DOMANDA
                    if int(msg) == 1 or int(msg) == 2 or int(msg) == 3: # verifica se ha messo un numero tra 1 e 3
                        if game.answer_menu(msg): #----------------------------PORTA CON DOMANDA
                            broadcast(bytes(game.get_question(), "utf8"))
                            game.set_status(GameStatus.QUESTION_PHASE)
                        else:
                            broadcast(bytes("%s è entrato nella porta sbagliata!." %nome, "utf8"))
                            game.removePlayer(game.get_current_player())
                            if game.check_end():
                                broadcast(bytes("%s Ha vinto." %game.check_winner().get_name(), "utf8"))
                            game.next_player()
                            game.set_status(GameStatus.STARTED) # non ci va qui
                    else:
                        broadcast(bytes("Inserimento Errato, Scegli una porta tra 1, 2 , 3", "utf8"))
                        
                elif gameStatus == GameStatus.QUESTION_PHASE:
                    answer = msg.decode()
                    if game.answer_question(answer):
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

clients = {}
indirizzi = {}
HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
game = Game()
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
