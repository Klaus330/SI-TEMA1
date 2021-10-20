import socket

from aescipher import AESCipher

HEADER = 32
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
PUBLIC_KEY = 'securiatatea_informatiei'
PRIVATE_KEY = ''
ENCRYPTION_MODE = ''
PUBLIC_KEY = 'securiatatea_informatiei'.encode(FORMAT)
IV = "aabbccddeeffgghh".encode(FORMAT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(message):
    lengthToSend = str(len(message)).encode(FORMAT)
    lengthToSend += b' ' * (HEADER - len(message))
    client.send(lengthToSend)
    client.send(message)

def receive():
    messageLength = client.recv(HEADER)
    if(messageLength):
        messageLength = int(messageLength)
        message = client.recv(messageLength)
        print(f"[SERVER] {message}")        
        if message == DISCONNECT_MESSAGE:
            exit()
        return message


def decryptReceivedMessage(blocks):
    
    cipher = AESCipher(PRIVATE_KEY, IV, HEADER)
    return cipher.decrypt(blocks, ENCRYPTION_MODE.decode())

def start():
    global PRIVATE_KEY, ENCRYPTION_MODE
    ENCRYPTION_MODE = receive()
    send("Mode".encode(FORMAT))
    PRIVATE_KEY = receive()
    print(f"[RECEIVED] ENCRYPTION: {ENCRYPTION_MODE.decode()}")
    print(f"[RECEIVED] KEY: {PRIVATE_KEY}")
    send("OK".encode(FORMAT))

    blocks = []
    line = receive()
    while line: 
        blocks.append(line)
        line = receive()
            
    print("Mesajul criptat primit este:")    
    print(blocks)
    print()
    print("Mesajul decriptat este:")
    print(decryptReceivedMessage(blocks))


    print(f"[CLIENT] FILE TRANSFERED")

start()