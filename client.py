"""
Created on Wed Jan 20 10:03:25 2021

@author: Lucas.singier
"""
import socket


IP = "127.0.0.1"
PORT = 1234

inputPseudo = input("Veuillez entrer votre pseudo: ")

# Creation de la socket + connection(ip,port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Mise en place des connecteurs non blocants car la socket est utilisée à 
# chaque fois et sans cet element le client ne va envoyer qu'un seul message
client_socket.setblocking(False)

# Envoie du pseudo au serveur, encodage des variables 
#car soucis de type sur le bytes alors qu'on a du string
pseudo = inputPseudo.encode('utf-8')
# le header prend la valeur de la taille du message
taillepseudo = f"{len(pseudo):<{10}}".encode('utf-8')
#envoi de la taille du pseudo et du pseudo au serveur
client_socket.send(taillepseudo + pseudo)

while True:
    # Attendre un message d'un utilisateur
    message = input(f'{inputPseudo} >> ')
    #Si le message n'est pas vide on l'envoie au serveur
    if message:
        message = message.encode('utf-8')
        #envoi du message et de sa taille au serveur
        taillemessage = f"{len(message):<{10}}".encode('utf-8')
        client_socket.send(taillemessage + message)