import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)
PUBLIC_KEY = 'securiatatea_informatiei'
PRIVATE_KEY = ''
ENCRYPTION_MODE = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    lengthToSend = str(len(message)).encode(FORMAT)
    lengthToSend += b' ' * (HEADER - len(message))
    client.send(lengthToSend)
    client.send(message)

def receive():
    messageLength = client.recv(HEADER).decode(FORMAT)
    if(messageLength):
        messageLength = int(messageLength)
        message = client.recv(messageLength).decode(FORMAT)
        print(f"[SERVER] {message}")        
        if message == DISCONNECT_MESSAGE:
            exit()
        return message

def start():
    ENCRYPTION_MODE = receive()
    send("Mode")
    PRIVATE_KEY = receive()
    print(f"[RECEIVED] ENCRYPTION: {ENCRYPTION_MODE}")
    print(f"[RECEIVED] KEY: {PRIVATE_KEY}")
    send("OK")

    while True:
        messageToSend = input();
        send(messageToSend);
        receive();

start();