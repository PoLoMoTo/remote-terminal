from socket import *

def main():
    host = 'localhost'
    port = 2222
    start((host, port))

def start(addr):
    # Create client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    clientSocket.connect(addr)

    clientSocket.send('login'.encode())
    while True:
        data = clientSocket.recv(1024).decode()
        userdata = input(data)
        clientSocket.send(userdata.encode())
        
main()