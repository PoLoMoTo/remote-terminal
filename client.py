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

    clientSocket.send('hello'.encode())

main()