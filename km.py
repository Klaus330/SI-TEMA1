import socket 
import threading

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PUBLIC_KEY = 'securiatatea_informatiei'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION-KM] {addr} connected.")
    sendResponse(conn, "Connected")
    
    receivedLength = conn.recv(HEADER).decode(FORMAT)
    if receivedLength:
        receivedLength = int(receivedLength)
        receivedMessage = conn.recv(receivedLength).decode(FORMAT)
        print(f"[{addr}] {receivedMessage}")
        sendResponse(conn, "Your KEY")

    conn.close()
        

def sendResponse(conn, response):
    responseLength = str(len(response)).encode(FORMAT)
    responseLength += b' ' * (HEADER - len(response))
    conn.send(responseLength)
    conn.send(response.encode(FORMAT))


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