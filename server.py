from socket import *

def main():
    host = ''
    port = 2222
    start((host, port))

def start(addr):
    # Open server socket
    welcomeSocket = socket(AF_INET, SOCK_STREAM)
    welcomeSocket.bind(addr)
    welcomeSocket.listen(5)

    # Take connections and direct to servlet
    while True:
        connection, addr = welcomeSocket.accept()
        servlet(connection)

# Servlet to handle connections
# This will help support threading later
def servlet(connection):
    data = connection.recv(1024)
    while data:
        print(data)
        data = connection.recv(1024)

main()