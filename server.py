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

    user = ''
    authenticated = False

    # Prompt for client login
    data = connection.recv(1024).decode()
    if data == 'login':
        connection.send('username'.encode())
    else:
        connection.send('error.auth'.encode())
        connection.close()
        return

    # Check valid user, prompt password
    data = connection.recv(1024).decode()
    if data.isalpha() and data in logins:
        user = data
        connection.send('password'.encode())
    else:
        connection.send('error.auth'.encode())
        connection.close()
        return

    # Validate user, break otherwise
    data = connection.recv(1024).decode()
    if data.isalnum() and  data == logins[user]:
        connection.send('success'.encode())
    else:
        connection.send('error.auth'.encode())
        connection.close()
        return

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

        if not data:
            break
        else:
            print('> ' + data)
            connection.send('success'.encode())

    connection.close()

if __name__ == "__main__":
    main(sys.argv[1:])
