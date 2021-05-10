#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from Game.game import Game
from Game.gameStatus import GameStatus


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
    while game.check_name_player(nome):
        client.send(bytes('Il nome %s è già stato utilizzato. Scegline un altro' % nome, "utf8"))
        nome = client.recv(BUFSIZ).decode("utf8")
    
    game.addPlayerToGameList(nome)

    client.send(bytes('Benvenuto %s! Se vuoi lasciare la Chat' % nome, "utf8"))
    client.send(bytes('Clicca il pulsante Pronto per dichiararti pronto \n', "utf8"))
    client.send(bytes('{quit} per uscire dal gioco', "utf8"))

    #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
    broadcast(bytes("%s si è unito alla chat!" % nome, "utf8"))
    #aggiorna il dizionario clients creato all'inizio
    clients[client] = nome
    
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ)
        
        if msg == QUIT:
            client.send(bytes("Si è scelto di uscire", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
            break
        elif msg == START and game.get_status() == GameStatus.STARTED:
            client.send(bytes("Gioco già cominciato!", "utf8"))
        elif msg == START and game.check_player_status(nome):
            client.send(bytes('Ti sei già dichiarato pronto', "utf8"))
        elif msg == START and game.get_status() != GameStatus.STARTED:
            game.setPlayerReady(nome)
            broadcast(bytes("Il giocatore %s è pronto" % nome, "utf8"))
            #incrementare il numero di giocatori pronti nel bottone [opzionale]
            game.start_game()
            if game.get_status() == GameStatus.STARTED:
                broadcast(bytes("\nTutti pronti, si parte!", "utf8"))
        else:
            broadcast(msg, nome+": ")

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
