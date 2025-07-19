import threading 
import socket

host = '127.0.0.1'
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

def broadcast(message):
    for cl in clients:
        cl.send(message)

def handle(cl):
    while True:
        try:
            message = cl.recv(1024)
            broadcast(message)
        except:
            index = clients.index(cl)
            clients.remove(cl)
            cl.close()
            alias = aliases[index]
            broadcast(f'{alias.decode("utf-8")} has left it'.encode('utf-8'))
            aliases.remove(alias)
            break     

def receive():
    while True:
        cl, address = server.accept()
        print(f'Connection established with {str(address)}')
        cl.send("alias?".encode('utf-8'))
        alias = cl.recv(1024)
        aliases.append(alias)
        clients.append(cl)
        print(f'The alias is {alias.decode("utf-8")}')
        broadcast(f'{alias.decode("utf-8")} has connected'.encode('utf-8'))
        cl.send("You are now connected!".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(cl,))
        thread.start()

receive()

