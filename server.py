import socket 
import threading
import socket 
import threading
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from aescipher import AESCipher

HEADER = 32
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PRIVATE_KEY = ''
PUBLIC_KEY = 'securiatatea_informatiei'.encode(FORMAT)
IV = "aabbccddeeffgghh".encode(FORMAT)
CONNECTION_SUCCESSFUL = 'OK'

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    sendResponse(conn, 'ECB'.encode('utf-8'))
    receiveMessage(conn, addr)
    sendResponse(conn, PRIVATE_KEY)
    msg = receiveMessage(conn, addr)
    print(f'{msg}')
    if msg != CONNECTION_SUCCESSFUL:
        print('WRONG CONNECTION')
        conn.close()
        return


    cryptedFileBlocks = getCryptedFiles()
    print(cryptedFileBlocks)
    for block in cryptedFileBlocks:
        sendResponse(conn, block)

    # file = open('file.txt', 'r')

    # for line in file:
    #     sendResponse(conn, line.encode(FORMAT))
    #     line = file.readline()
    #     print(f"READ: {line}")
    # file.close()

    print('[SERVER] FILE TRANSFERED')
    # sendResponse(conn,"!DISCONNECT".encode(FORMAT))

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
    responseLength += b' ' * (HEADER - len(responseLength))
    conn.send(responseLength)
    conn.send(response)


def fetchEncryptionKey():
    global PRIVATE_KEY
    clientKM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientKM.connect(("127.0.1.1", 5051))
    
    # receive welcome message
    messageLength = clientKM.recv(HEADER)
    if(messageLength):
        messageLength = int(messageLength.strip())
        message = clientKM.recv(messageLength)
        # print(f"[SERVER] {message}")

    # send identity
    message = "Give me THE KEY".encode(FORMAT)
    lengthToSend = str(len(message)).encode(FORMAT)
    lengthToSend += b' ' * (HEADER - len(message))
    clientKM.send(lengthToSend)
    clientKM.send(message)
    
    messageLength = clientKM.recv(HEADER)
    if(messageLength):
        messageLength = int(messageLength)
        message = clientKM.recv(messageLength)
        PRIVATE_KEY = decryptPrivateKey(message)
        print(f"[DECRYPTED KEY]{PRIVATE_KEY}")


def decryptPrivateKey(key):
    cipher = AES.new(PUBLIC_KEY, AES.MODE_ECB)
    return cipher.decrypt(key)


def getCryptedFiles():
    file = open('file.txt', 'r')
    print("LINES")
    cipher = AESCipher(PRIVATE_KEY, IV, HEADER)
    blocks = cipher.encryptECB(file.read())
    file.close()

    return blocks

def start():

    fetchEncryptionKey()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
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