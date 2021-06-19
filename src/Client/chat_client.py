# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:15:26 2021

@author: Gruppo Carboni - Ongaro

"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import Tk, Toplevel, Label, Entry, CENTER
from tkinter import Scrollbar, Button, DISABLED, END, NORMAL, Text
import time

class Client:

    def __init__(self):

        self.Window = Tk()
        self.Window.withdraw()
        
        # Schermata di login
        self.login = Toplevel()
        
        # Imposto il titolo della schermata
        self.login.title("Login")
        
        self.login.resizable(width=False,
                             height=False)
        self.login.geometry('500x500')

        self.login.configure(width=400,
                             height=300,
                             bg="#17202A")

        self.pls = Label(self.login,
                         text="Inserisci un nome per entrare",
                         justify=CENTER,
                         font="Helvetica 14 bold",
                         bg='#17202A',
                         fg='#AEB9E6')

        self.pls.place(relheight = 0.15, 
                       relx = 0.23, 
                       rely = 0.07)

        # Casella di testo dove l'utente inserirà il nome
        self.entryName = Entry(self.login, font="Helvetica 14")

        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.30,
                             rely = 0.30)

        # Imposto il focus sulla casella di testo
        self.entryName.focus()

        # Creazione del bottone - alla pressione di esso verrà invocata
        # la funzione goAhead
        self.go = Button(self.login,
                         text="Accedi",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()),
                         bg='#8CAEE6',
                         fg='#ffffff')

        self.go.place(relx = 0.43, 
                      rely = 0.55)
        
        self.errorLabel = Label(self.login,
                         text="",
                         justify=CENTER,
                         font="Helvetica 10",
                         bg='#17202A',
                         fg='#AEB9E6')
        
        self.errorLabel.place(relheight = 0.15, 
                       relx = 0.0, 
                       rely = 1)
        
        self.Window.mainloop()

    """ Passaggio alla schermata successiva in caso di nome inserito non vuoto """
    def goAhead(self, name):
        if name != "":  # Se il nome non è vuoto creo una nuova finestra
            client_socket.send(bytes(name, FORMAT))
            self.login.destroy()
            self.layout(name)

            # Faccio partire i thread per ascoltare i messaggi in entrata
            rcv = Thread(target=self.receive)
            rcv.start()

    """ Creazione layout della schermata principale del gioco """
    def layout(self, name):

        self.name = name

        self.Window.deiconify()
        self.Window.title("CHAT GAME")
        
        #Funzione da eseguire quando viene cliccata la x
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.Window.resizable(width=False,
                              height=False)

        self.Window.configure(width=670,
                              height=750,
                              bg="#17202A")

        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
                                text="Invia",
                                font="Helvetica 10 bold",
                                width=20,
                                bg='#8CAEE6',
                                command=lambda: 
                                    self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.readyBtn = Button(self.labelBottom,
                               text="Pronto",
                               font="Helvetica 10 bold",
                               width=20,
                               bg='#8CAEE6',
                               command=self.ready)

        self.readyBtn.place(relx=0.77,
                            rely=0.040,
                            relheight=0.03,
                            relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # Crea la scrollbar
        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    """ Invio messaggi al server """
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.entryMsg.delete(0, END)
        if msg == "": # Blocco invio di messaggi vuoti
            return
        client_socket.send(bytes(msg, FORMAT))
        if msg == "{quit}":
            self.close()

    """ Ricezione dei messaggi """
    def receive(self):
        while True:
            try:
                msg = client_socket.recv(1024).decode(FORMAT)

                # Se il server restituisce errore blocca la scrittura del nome
                if msg == 'Errore':
                    print("Gioco Partito")
                    i = 5
                    while i != 0:
                        print("Addio tra {} secondi", i)
                        time.sleep(i)
                    self.close()
                else:
                    # Inserisci i messaggi alla textbox
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, msg + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except OSError:
                # Scrittura del messaggio di errore nel caso in cui ci sia un errore
                print("An error occured!")
                client_socket.close()
                break
    
    """ Invio Messaggio {start} alla pressione del bottone Pronto"""
    def ready(self, event=None):
        self.sendButton("{start}")
    
    """ Chiusura applicazione e del socket"""
    def close(self):
        client_socket.close()
        self.Window.quit()
        self.Window.destroy()
        
    def on_closing(self):
        client_socket.send(bytes('{quit}', FORMAT))
        self.close()
        
# ----Connessione al Server----
HOST = "127.0.0.1"
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
FORMAT = "utf8"
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# ----Lancio l'applicativo----
c = Client()
