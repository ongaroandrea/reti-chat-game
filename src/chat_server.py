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
def accept_in_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)

        #Se il gioco è gia iniziato non accetto la connessione
        if game.get_status() != GameStatus.NOT_STARTED: 
            client.close()
            print("Gioco già iniziato. Impossibile far entrare un nuovo giocatore")
            client.send(bytes("Errore", "utf8"))
        else:
            # ci serviamo di un dizionario per registrare i client
            indirizzi[client] = client_address
            # diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=handle_client_request, args=(client,)).start()


"""La funzione seguente gestisce la connessione di un singolo client."""
def handle_client_request(client):  # Prende il socket del client come argomento della funzione.

    global matchIndex
    global currentPlayer
    global game
    global gameStatus

    nome = client.recv(BUFSIZ).decode("utf8")  # --------------------------------SCELTA NOME
    while game.check_name_player(nome):
        # se il nome è già presente ci aggiunge un _ per distinguere i nomi
        nome = "{}{}".format(nome, "_")

    # CONTROLLO STATO GIOCO
    if game.get_status() != GameStatus.NOT_STARTED:
        client.send(bytes("Il gioco è attualmente in esecuzione - RIPROVA PIU' TARDI", "utf8"))
        client.close()
        return

    game.addPlayerToGameList(nome)

    # BENVENUTO
    if len(game.get_players()) > 1:
        client.send(bytes("Sono già presenti i seguenti giocatori: \n", "utf8"))
        for player in game.get_players():
            if player.get_name() != nome: 
                client.send(bytes("{}: {}\n".format(player.get_name(), player.get_role()), "utf8"))
                
    client.send(bytes('Benvenuto %s! Se vuoi lasciare la Chat' % nome, "utf8"))
    client.send(bytes('\nClicca il pulsante Pronto per dichiararti pronto', "utf8"))
    client.send(bytes('\n{quit} per uscire dal gioco', "utf8"))
    client.send(bytes('\nIl tuo ruolo è %s'%game.get_player(nome).get_role(), "utf8"))

    broadcast("%s si è unito alla chat!" % nome)
    broadcast("Il ruolo di {} è {}.".format(nome, game.get_player(nome).get_role()))
    clients[client] = nome

    # si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        gameStatus = game.get_status()

        # --------COMANDI--------
        # QUIT
        if msg == QUIT:
            game.removePlayer(game.get_player(nome))
            broadcast("%s ha abbandonato la Chat." % nome)
            if (gameStatus != GameStatus.NOT_STARTED):
                broadcast("La partita termina.")
                end_function()
            client.close()
            del clients[client]
            break
        # START se è gia cominciato
        elif msg == START and gameStatus != GameStatus.NOT_STARTED:
            client.send("Gioco già cominciato!".encode())
        # START se è gia pronto
        elif msg == START and game.check_player_ready(nome):
            client.send('Ti sei già dichiarato pronto'.encode())
        # START
        elif msg == START and gameStatus != GameStatus.STARTED:
            game.setPlayerReady(nome)
            broadcast("Il giocatore %s è pronto" % nome)
            # Se i giocatori sono tutti pronti parte il gioco
            if game.get_status() == GameStatus.STARTED:
                broadcast("\nTutti pronti, si parte!")
                matchIndex += 1
                #il gioco iniza
                game.start_game()
                #inzia il timer del gioco principale
                start_countdown(GAME_TIME, GameStatus.ENDED, True, None, end_function)
        # BROADCAST MESSAGGIO (se non è un comando)
        else:
            broadcast("{}: {}".format(nome, msg))

        currentPlayer = ""
        gameStatus = game.get_status()
        if gameStatus != GameStatus.NOT_STARTED and gameStatus != GameStatus.ENDED:  # se il gioco è partito
            currentPlayer = game.get_current_player().get_name()

            # GIOCO INIZIATO, stampo testo per la scelta della porta
            if gameStatus == GameStatus.STARTED:
                broadcast("\nTurno di: %s. " % currentPlayer)
                broadcast("\nScegli una porta tra 1, 2 e 3.")
                game.set_status(GameStatus.MENU_PHASE)
            else:
                # se chi scrive è chi deve dare una risposta
                if currentPlayer == nome:
                    # è stata scelta la porta
                    if gameStatus == GameStatus.MENU_PHASE:
                        # controllo se il messaggio inviato è un numero tra 1, 2 e 3
                        if msg.isnumeric() and int(msg) == 1 or int(msg) == 2 or int(msg) == 3:
                            # il giocatore è entrato in una porta con la domanda
                            if game.answer_menu(msg):
                                # stampo domanda
                                broadcast(game.get_question())
                                game.set_status(GameStatus.QUESTION_PHASE)
                                gameStatus = GameStatus.QUESTION_PHASE
                                # timer di 5 secondi per rispondere alla domanda
                                start_countdown(5, GameStatus.MENU_PHASE, False, GameStatus.QUESTION_PHASE,
                                                stop_time_answer)
                            #il giocatore è entrato nella porta con la bomba
                            else:
                                broadcast("%s è entrato nella porta sbagliata!." % nome)
                                game.next_player()
                                game.killPlayer(game.get_player(currentPlayer))
                                # se non rimane solo un giocatore il gioco termina
                                if game.check_end():
                                    game.set_status(GameStatus.ENDED)
                                    gameStatus = GameStatus.ENDED
                                    end_function()
                                # se rimane più di un giocatore continuo il gioco
                                else:
                                    game.set_status(GameStatus.STARTED)
                                    broadcast("%s se ne va!." % nome)
                                    currentPlayer = game.get_current_player().get_name()
                                    broadcast("\nTurno di: %s. " % currentPlayer)
                                    broadcast("\nScegli una porta tra 1, 2 e 3.")
                                    game.set_status(GameStatus.MENU_PHASE)
                                    gameStatus = GameStatus.MENU_PHASE
                        # se il messaggio per la scelta della porta non è un numero tra 1, 2 e 3
                        else:
                            client.send(bytes("Inserimento Errato, Scegli una porta tra 1, 2 , 3", "utf8"))
                    # se è stata scelta la risposta alla domanda
                    elif gameStatus == GameStatus.QUESTION_PHASE:
                        # se la risposta è corretta
                        if game.answer_question(msg):
                            game.add_points()
                            broadcast("Risposta esatta, punteggio aumentato!")
                        # se la risposta è sbagliata
                        else:
                            game.remove_points()
                            broadcast("Risposta errata!")
                        # passo al prossimo giocatore
                        game.next_player()
                        currentPlayer = game.get_current_player().get_name()
                        broadcast("\nTurno di: %s. " % currentPlayer)
                        broadcast("Scegli una porta tra 1, 2 e 3.")
                        game.set_status(GameStatus.MENU_PHASE)
                # se chi scrive non è chi deve dare una risposta stampo errore
                else:
                    client.send(bytes("Non è il tuo turno", "utf8"))


""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso + msg, "utf8"))

""" La funzione countdown crea un timer di specificata durata, argomenti:
    quitStatus: specifica lo stato nel quale il timer deve fermarsi
    alwaysDo: specifica se va sempre fatto o vanno fatti controlli aggiuntivi
    doStatus: specifica quando bisogna eseguire la funzione specificata
"""
def countdown(duration, quitStatus, alwaysDo, doStatus, function):
    thisCountdownMatchIndex = matchIndex
    thisPlayer = currentPlayer
    # il countdown si ferma quando finisce i secondi o quando il gioco arriva allo stato definito
    while duration > 0 and gameStatus != quitStatus:
        tm.sleep(1)
        duration -= 1
    # timer ended - eseguo la funzione specificata quando il flag alwaysDo è true
    # oppure quando sono in doStatus ed il giocatore è lo stesso
    if alwaysDo and thisCountdownMatchIndex == matchIndex and game.get_status() != GameStatus.ENDED and game.get_status() != GameStatus.NOT_STARTED:
        function()
    else:
        actualGameStatus = game.get_status()
        if actualGameStatus == doStatus and thisCountdownMatchIndex == matchIndex and thisPlayer == currentPlayer:
            function()

""" Avvia un thread per il countdown """
def start_countdown(duration, quitStatus, alwaysDo, doStatus, function):
    countdown_thread = threading.Thread(target=countdown, args=(duration, quitStatus, alwaysDo, doStatus, function,))
    countdown_thread.daemon = True  # rendo il thread deamon, alla chiusura del server morirà
    countdown_thread.start()

""" Funzione da eseguire quando termina il tempo per rispondere alla domanda """
def stop_time_answer():
    broadcast("Tempo Scaduto per rispondere")
    game.remove_points()
    game.next_player()
    currentPlayer = game.get_current_player().get_name()
    broadcast("\nTurno di: %s. " % currentPlayer)
    broadcast("\nScegli una porta tra 1, 2 e 3.")
    game.set_status(GameStatus.MENU_PHASE)

""" Funzione che fa terminare il gioco e stampare la classifica """
def end_function():
    rank = game.get_rank()
    winner = rank[0]
    broadcast("%s Ha vinto." % winner.get_name())
    tm.sleep(1)
    game.set_status(GameStatus.ENDED)
    # stampa classifica
    broadcast("\nGioco Terminato. Classifica:", "utf8")
    i = 0
    for player in rank:
        i += 1
        broadcast("\n{}°: {}, {}, {}\n".format(i, player.get_name(), player.get_score(), player.get_status()))
        tm.sleep(1)
    # reset gioco
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
GAME_TIME = 300
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
    ACCEPT_THREAD = Thread(target=accept_in_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
