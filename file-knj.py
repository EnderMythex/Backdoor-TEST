import socket
import webbrowser

def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f'[*] Listening on {host}:{port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'[+] Connection from {addr[0]}:{addr[1]}')

        while True:
            command = input('[?] Command: ')
            if command == 'exit':
                break
            elif command.startswith('openurl:'):
                url = command.split('openurl:')[1]
                webbrowser.open(url)
                response = 'Opened URL in default browser'
            elif command.startswith('openfile:'):
                file_name = command.split('openfile:')[1]
                try:
                    with open(file_name, 'r') as file:
                        for line in file:
                            webbrowser.open(line.strip())
                    response = 'Opened all URLs in file'
                except FileNotFoundError:
                    response = 'File not found'
            else:
                client_socket.send(command.encode())
                response = client_socket.recv(1024).decode()

            print(f'[!] Response: {response}')

        client_socket.close()

if __name__ == '__main__':
    start_server()
