import socket
import threading

#  pscp socketClient.py syank@192.168.15.6:pythonFiles/socketClient.py

host = input("Insira o IP do HOST: ")
port = int(input("Insira a porta a ser ouvida: "))
connections = {}


def closeConnection(clientSocket):
    if clientSocket in connections:
        del connections[clientSocket]


def broadcastMessage(message, clientSocket):
    for connection in connections:
        if connection != clientSocket:
            try:
                connection.sendall(bytearray(message, "utf-8"))

            except ConnectionAbortedError:
                closeConnection(connection)


def listenClientSocket(clientSocket, clientAddress):
    while True:
        try:
            message = clientSocket.recv(1024)

            if message:
                print(f"{clientAddress}, {connections[clientSocket]}: {message.decode('utf-8')}")

                messageToBroadcast = f"De {connections[clientSocket]}: {message.decode('utf-8')}"

                broadcastMessage(messageToBroadcast, clientSocket)

        except ConnectionResetError:
            closeConnection(clientSocket)
            break


def runServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((host, port))
        serverSocket.listen(5)

        print("Servidor inicializado com sucesso! Recebendo conexões...")

        while True:
            clientSocketConnection, clientAddress = serverSocket.accept()

            registerMessage = clientSocketConnection.recv(1024)

            clientName = registerMessage.decode(encoding="utf-8").split(":")[1]

            connections[clientSocketConnection] = clientName

            print(f"Nova conexão de: {clientAddress}, como \"{clientName}\"")

            threading.Thread(target=listenClientSocket, args=[clientSocketConnection, clientAddress]).start()


runServer()
