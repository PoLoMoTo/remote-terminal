from socket import *
import signal

def main():
    host = 'localhost'
    port = 2222
    start((host, port))

def start(addr):
    # Create client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    clientSocket.connect(addr)

    # Prompt server for login
    clientSocket.send('login'.encode())

    # User input, exit on exit received
    userdata = ''
    while userdata != 'exit':
        data = clientSocket.recv(1024).decode()
        userdata = input(data)
        clientSocket.send(userdata.encode())

    # Close socket
    clientSocket.close()

main()
