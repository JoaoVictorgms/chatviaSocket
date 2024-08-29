import socket
import threading
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


clients = {}
def handle_client(client_socket):
    try:

        nickname_message = client_socket.recv(1024).decode()
        if not nickname_message.startswith("! nick"):
            client_socket.send("! error Você precisa definir um nickname primeiro.".encode())
            client_socket.close()
            return

        nickname = nickname_message.split()[2]
        clients[nickname] = client_socket

        users_message = "! users " + " ".join(clients.keys())
        client_socket.send(users_message.encode())

        broadcast(f"! msg Servidor {nickname} entrou no chat.")

        while True:
            message = client_socket.recv(1024).decode()
            if message.startswith("! sendmsg"):
                broadcast(f"! msg {nickname} {message.split(' ', 1)[1]}")
            elif message.startswith("! changenickname"):
                new_nickname = message.split()[1]
                if new_nickname in clients:
                    client_socket.send("! error Nickname já em uso.".encode())
                else:
                    broadcast(f"! changenickname {nickname} {new_nickname}")
                    clients[new_nickname] = clients.pop(nickname)
                    nickname = new_nickname
            elif message.startswith("! poke"):
                poked_user = message.split()[1]
                if poked_user in clients:
                    broadcast(f"! poke {nickname} {poked_user}")
                else:
                    client_socket.send("! error Usuário não encontrado.".encode())
    except:
        pass
    finally:
        client_socket.close()
        del clients[nickname]
        broadcast(f"! msg Servidor {nickname} saiu do chat.")

def broadcast(message):
    for client_socket in clients.values():
        client_socket.send(message.encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Nova conexão de {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
