import threading 
import socket

alias = input("Choose an alias: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))

def c_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error occurred. Connection closed.")
            client.close()
            break

def c_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=c_receive)
receive_thread.start()

sender_thread = threading.Thread(target=c_send)
sender_thread.start()


