import socket
import threading

host = input("Insira o IP do HOST: ")
port = int(input("Insira a porta a ser ouvida: "))
clientName = input("Insira seu nome de usuário: ")


def receiveMessages(clientSocket):
    while True:
        message = clientSocket.recv(1024)

        if message:
            print(message.decode(encoding="utf-8"))

        else:
            break


def initializeClient():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((host, port))

        clientSocket.sendall(bytearray(f"clientName:{clientName}", "utf-8"))

        threading.Thread(target=receiveMessages, args=[clientSocket]).start()

        print("Conectado ao chat!")

        while True:
            message = input()

            if message == "<sair>":
                break

            clientSocket.sendall(bytearray(message, "utf-8"))
        

initializeClient()
