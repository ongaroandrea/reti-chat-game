# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:15:26 2021

@author: Gruppo Carboni - Ongaro

"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import Tk, Toplevel, Label, Entry, CENTER
from tkinter import Scrollbar, Button, DISABLED, END, NORMAL, Text,N

class GUI:
    # constructor method
    def __init__(self):
        
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False,
                            height = False)
        self.login.geometry('500x500')  

        self.login.configure(width = 400,
                            height = 300,
                            bg = "#17202A")
        # create a Label
        self.pls = Label(self.login,
                    text = "Inserisci un nome per entrare",
                    justify = CENTER,
                    font = "Helvetica 14 bold")
        
        self.pls.grid(column=1,row=1,columnspan=2, sticky=N)
        #self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)
        # create a Label
        #self.labelName = Label(self.login, text = "Nome: ", font = "Helvetica 12")
        #self.labelName.place(relheight = 0.2, relx = 0.1, rely = 0.4)
        
        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                            font = "Helvetica 14")
        
        self.entryName.grid(column=1,row=3,columnspan=2)
        #self.entryName.place(relwidth = 0.4, relheight = 0.12, x=175, y=150)
        
        # set the focus of the curser
        self.entryName.focus()
        
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                        text = "Accedi",
                        font = "Helvetica 14 bold",
                        command = lambda: self.goAhead(self.entryName.get()))
        
        self.go.grid(column=1,row=5,columnspan=2)
        
        #self.go.place(relx = 0.4, rely = 0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        client_socket.send(bytes(name,FORMAT))
        self.login.destroy()
        self.layout(name)
        
        # the thread to receive messages
        rcv = Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHAT GAME")
        self.Window.resizable(width = False,
                            height = False)
        self.Window.configure(width = 670,
                            height = 750,
                            bg = "#17202A")
        
        self.labelHead = Label(self.Window,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            text = self.name ,
                            font = "Helvetica 13 bold",
                            pady = 5)
        
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                        width = 450,
                        bg = "#ABB2B9")
        
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        
        self.textCons = Text(self.Window,
                            width = 20,
                            height = 2,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            font = "Helvetica 14",
                            padx = 5,
                            pady = 5)
        
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
        
        self.labelBottom = Label(self.Window,
                                bg = "#ABB2B9",
                                height = 80)
        
        self.labelBottom.place(relwidth = 1,
                            rely = 0.825)
        
        self.entryMsg = Entry(self.labelBottom,
                            bg = "#2C3E50",
                            fg = "#EAECEE",
                            font = "Helvetica 13")
        
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
        
        self.entryMsg.focus()
        
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Invia",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda:  self.sendButton(self.entryMsg.get()))
        
        self.buttonMsg.place(relx = 0.77,
                            rely = 0.008,
                            relheight = 0.03,
                            relwidth = 0.22)
        
        self.readyBtn = Button(self.labelBottom,
                                text = "Pronto",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = self.ready)
        
        self.readyBtn.place(relx = 0.77,
                            rely = 0.040,
                            relheight = 0.03,
                            relwidth = 0.22)
        
        self.textCons.config(cursor = "arrow")
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        
        scrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(state = DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.entryMsg.delete(0, END)
        print(msg)
        client_socket.send(bytes(msg, FORMAT))
        if msg == "{quit}":
            client_socket.close()
            self.Window.quit()
            self.Window.destroy()

    # function to receive messages
    def receive(self):
        while True:
            try:
                msg = client_socket.recv(1024).decode(FORMAT)
                
                # if the messages from the server is NAME send the client's name
                if msg == 'Errore':
                     #client_socket.send(bytes(msg, FORMAT))
                     print("Gioco Partito")
                else:
                    # insert messages to text box
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, msg+ "\n\n")
                    
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except OSError:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client_socket.close()
                break

    def ready(self,event=None):
        self.sendButton("{start}")

#----Connessione al Server----
HOST = "127.0.0.1"
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
FORMAT = "utf8"
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

g = GUI()