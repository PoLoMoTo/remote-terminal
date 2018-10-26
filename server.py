from socket import *

logins = {
    'test': 'cab123'
}

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
    user = ''

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

    data = connection.recv(1024).decode()
    while data and data != 'exit':
        print(data)
        connection.send('success'.encode())
        data = connection.recv(1024)
    connection.close()

main()