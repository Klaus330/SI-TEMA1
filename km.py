import socket 
import threading
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import base64
import secrets
from aescipher import AESCipher


HEADER = 32
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PUBLIC_KEY = "securiatatea_informatiei".encode(FORMAT)
IV = "aabbccddeeffgghh".encode(FORMAT)



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION-KM] {addr} connected.")
    sendResponse(conn, "Connected".encode(FORMAT))

    receivedLength = conn.recv(HEADER).decode(FORMAT)
    if receivedLength:
        receivedLength = int(receivedLength)
        receivedMessage = conn.recv(receivedLength).decode(FORMAT)
        print(f"[{addr}] {receivedMessage}")

        private_key = generatePrivateKey()
        print(f"\n[GENERATED-KEY] {private_key}")
        sendResponse(conn, private_key)

    conn.close()
        

def generatePrivateKey():
    key = secrets.token_bytes(HEADER)
    print(f"[PRIVATE-KEY] {key}")
    cipher = AES.new(PUBLIC_KEY, AES.MODE_ECB)
    return cipher.encrypt(key)

def sendResponse(conn, response):
    responseLength = str(len(response)).encode(FORMAT)
    responseLength += b' ' * (HEADER - len(responseLength))
    conn.send(responseLength)
    
    conn.send(response)


def start():
    server.listen()
    print(f"[LISTENING-KM] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS-KM] {threading.activeCount() - 1}")


print("[STARTING-KM] server is starting...")
start()