#!/usr/bin/env python3
"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone.
Corso di Programmazione di Reti - Università di Bologna"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from Player.player import Player
from Player.player import PlayerStatus

gameReady = False
""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accetta_connessioni_in_entrata():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
        if gameReady == True:
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
    list.append(Player(nome, "Burattinaio"))

    benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi: \n {start} per dichiararti pronto \n {quit} per uscire.' % nome
    client.send(bytes(benvenuto, "utf8"))
    msg = "%s si è unito all chat!" % nome
    #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
    broadcast(bytes(msg, "utf8"))
    #aggiorna il dizionario clients creato all'inizio
    clients[client] = nome
    
#si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ)
        print(msg)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, nome+": ")
            global gameReady
            gameReady = True
            if msg != bytes("{start}", "utf8"):
                for p in list: #Imposto il giocatore corrente come PRONTO
                    if p.getName() == nome:
                        p.getStatus = PlayerStatus.READY 
                    
            for p in list: #Controllo se tutti i giocatori sono pronti
                if p.getStatus == PlayerStatus.NOT_READY :
                    gameReady = False
                    break                
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
            break

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)
    for obj in list:
        print(obj.getName())

        
clients = {}
indirizzi = {}
list = []
HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
