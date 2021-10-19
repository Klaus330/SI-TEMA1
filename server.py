import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PRIVATE_KEY = ''
PUBLIC_KEY = 'securiatatea_informatiei'
CONNECTION_SUCCESSFUL = 'OK'

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    sendResponse(conn, 'ECB')
    receiveMessage(conn, addr)
    sendResponse(conn, PRIVATE_KEY)
    msg = receiveMessage(conn, addr)
    print(f'{msg}')
    if msg != CONNECTION_SUCCESSFUL:
        print('WRONG CONNECTION')
        conn.close()
        return;

    file = open('file.txt', 'r')

    for line in file:
        sendResponse(conn, line)
        line = file.readline()
        print(f"READ: {line}")
    file.close()

    print('[SERVER] FILE TRANSFERED')
    sendResponse(conn,"!DISCONNECT")

    conn.close()
        

def receiveMessage(conn, addr):
    receivedLength = conn.recv(HEADER).decode(FORMAT)
    if receivedLength:
        receivedLength = int(receivedLength)
        receivedMessage = conn.recv(receivedLength).decode(FORMAT)
        print(f"[{addr}] {receivedMessage}")
        return receivedMessage

def sendResponse(conn, response):
    responseLength = str(len(response)).encode(FORMAT)
    responseLength += b' ' * (HEADER - len(response))
    conn.send(responseLength)
    conn.send(response.encode(FORMAT))


def fetchEncryptionKey():
    global PRIVATE_KEY
    clientKM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientKM.connect(("192.168.56.1", 5051))
    # receive welcome message
    messageLength = clientKM.recv(HEADER).decode(FORMAT)
    if(messageLength):
        messageLength = int(messageLength)
        message = clientKM.recv(messageLength).decode(FORMAT)
        print(f"[SERVER] {message}")
    # send identity
    message = "Give me THE KEY".encode(FORMAT)
    lengthToSend = str(len(message)).encode(FORMAT)
    lengthToSend += b' ' * (HEADER - len(message))
    clientKM.send(lengthToSend)
    clientKM.send(message)
    
    messageLength = clientKM.recv(HEADER).decode(FORMAT)
    if(messageLength):
        messageLength = int(messageLength)
        message = clientKM.recv(messageLength).decode(FORMAT)
        PRIVATE_KEY = message
        print(f"[SERVER] {message}")
    

def start():

    fetchEncryptionKey()
    print(f"KEY: {PRIVATE_KEY}")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()