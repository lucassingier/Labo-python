"""
Created on Wed Jan 20 10:15:31 2021

@author: Lucas.singier
"""
import socket
import select

IP = "127.0.0.1"
PORT = 1234
# Creation de la socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On set les options du socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Binding de la socket = permet de lier une communication par une adresse et un port
server_socket.bind((IP, PORT))

# Mise en place d'un serveur pour écouter les connexions
server_socket.listen()
#Liste des socket
listeSocket = [server_socket]

# création d'un dictionnaire-> cle=pseudo,valeur=message
clients = {}
#Affiche sur le serveur que le serveur fonctionne bien et qu'il attend des conenxions
print(f'Le serveur fonctionne sur {IP}:{PORT} \n')

# fonction de récupération du message
def recup_message(client_socket):
    try:
        # on recois la taille du message
        tailledumessage = client_socket.recv(10)
        # Si on ne reçois rien..
        if not len(tailledumessage):
            return False
        # Convertis en int la taille du message (etait en byt)
        tailledumessageint = int(tailledumessage.decode('utf-8'))
        #On retourne donc un dictionnaire
        return {'cle': tailledumessage, 'mess': client_socket.recv(tailledumessageint)}
    except:
        # Exception si le client ferme sa connection ctrl+c
        return False
while True:
    #Connecteur
    lecturesockets, _, exceptionssockets = select.select(listeSocket, [], listeSocket)
    # parcours la liste de socket
    for sock in lecturesockets:
        #Accepte les nouvelles connections
        if sock == server_socket:
            client_socket, client_address = server_socket.accept()
            # Recuperation du pseudo
            cli_mess = recup_message(client_socket)
            # Si le client se deconnecte
            if cli_mess is False:
                continue
            # apprend le client dans la liste de socket
            listeSocket.append(client_socket)
            clients[client_socket] = cli_mess
            print('Nouvel arrivant: {}'.format(cli_mess['mess'].decode('utf-8')))
        # Si il existe une socket on envoie un message
        else:
            # Utilisation de la fonction de reception de messages
            message = recup_message(sock)
            # Si client se deconnecte
            if message is False:
                print('Déconnexion de {}'.format(clients[sock]['mess'].decode('utf-8')))
                # Enleve le client de la liste
                listeSocket.remove(sock)
                # suppression dans la liste client
                del clients[sock]
                continue
            # Pour savoir qui envoie le message
            user = clients[sock]
            print(f'{user["mess"].decode("utf-8")}: {message["mess"].decode("utf-8")}')
            # On parcours la liste des clients socket
            for clisock in clients:
                if clisock != sock:
                    # Affichage du pseudo et de son message
                    clisock.send(user['cle'] + user['mess'] + message['cle'] + message['mess'])

