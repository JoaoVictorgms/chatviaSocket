import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Conexão perdida com o servidor.")
            client_socket.close()
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    nickname = input("Escolha seu nickname: ")
    client_socket.send(f"! nick {nickname}".encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        command = input()
        client_socket.send(command.encode())

if __name__ == "__main__":
    main()
