from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RD, MSG_DONTWAIT
import signal
import sys

logins = {
    'test': 'cab123'
}

def main(argv):
    if argv[0].isnumeric():
        port = int(argv[0])
        start(('', port))
    else:
        print('Invalid arguments!')

def start(addr):
    # Open server socket
    welcomeSocket = socket(AF_INET, SOCK_STREAM)
    welcomeSocket.bind(addr)
    welcomeSocket.listen(5)
    processes = []

    # Stop accepting connections and wait for all connections to close
    # on interrupt
    try:
        # Take connections and direct to servlet
        while True:
            connection, addr = welcomeSocket.accept()
            P = Process(target=servlet, args=(connection,))
            P.start()
            processes.append(P)
    except KeyboardInterrupt:
        # Refuse further connection requests
        welcomeSocket.shutdown(SHUT_RD)
        # Wait for existing connections to disconnect
        while processes:
            processes.pop().join()
        # Close the socket
        welcomeSocket.close()

# Servlet to handle connections
# This will help support threading later
def servlet(connection):
    # Redirect keyboard interupt signal for children
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Credential data
    user = ''
    authenticated = False

    # Client interaction loop
    while True:
        # Receive user data
        data = connection.recv(1024).decode()

        # Receive until the buffer is empty
        if data and len(data) == 1024:
            furtherData = connection.recv(1024, MSG_DONTWAIT).decode()
            data += furtherData
            while furtherData and len(furtherData) == 1024:
                furtherData = connection.recv(1024, MSG_DONTWAIT).decode()
                data += furtherData

        # Exit if connection closes
        if not data:
            break

        # Block access until authenticated
        elif not authenticated:
            # Validate username and prompt for password
            if data[:9] == 'username.':
                if data[9:].isalpha() and data[9:] in logins:
                    user = data[9:]
                    connection.send('password'.encode())
                else:
                    connection.send('error.auth'.encode())
                    break

            # Validate password
            elif data[:9] == 'password.':
                if data[9:].isalnum() and data[9:] == logins[user]:
                    authenticated = True
                    connection.send('success'.encode())
                else:
                    connection.send('error.auth'.encode())
                    break

            # No username, prompt for username
            elif not user:
                connection.send('username'.encode())

            # Username but not authenticated, prompt for password
            else:
                connection.send('password'.encode())

        # Allow authenticated user to access services
        elif authenticated:
            print('> ' + data)
            connection.send('success'.encode())

    connection.close()

if __name__ == "__main__":
    main(sys.argv[1:])
