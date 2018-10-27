from socket import socket, AF_INET, SOCK_STREAM
import sys

def main(argv):
    if argv[0].isalpha() and argv[1].isnumeric():
        host = argv[0]
        port = int(argv[1])
        start((host, port))
    else:
        print('Invalid arguments!')

def start(addr):
    # Create client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    clientSocket.connect(addr)

    # Prompt server for login (Required to start connection)
    clientSocket.send('login'.encode())

    # Running connection loop
    while True:

        # Wait for data from the server
        data = clientSocket.recv(1024).decode()

        # Act on server response
        if data == 'username':
            userdata = 'username.' + input('Username: ')
        elif data == 'password':
            userdata = 'password.' + input('Password: ')
        elif data[:6] == 'error.':
            print('Received error: ' + data[6:])
            break
        elif data == 'success':
            userdata = input('> ')
        else:
            print('Unknown response: ' + data)
            break

        # If the user requested exit break the loop
        if userdata == 'exit':
            break

        # Send the client data to the server
        clientSocket.send(userdata.encode())

    # Close socket
    clientSocket.close()

if __name__ == "__main__":
    main(sys.argv[1:])
