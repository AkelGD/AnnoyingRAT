import socket
import os

def connect_to_server(host='0.0.0.0', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    while True:
        command = input("Enter command: ")
        client.send(command.encode('utf-8'))
        
        if command.startswith('upload '):
            file_name = command.split(' ', 1)[1]
            if os.path.exists(file_name):
                with open(file_name, 'rb') as f:
                    file_data = f.read()
                client.sendall(file_data)
                print(f"File '{file_name}' uploaded.")
            else:
                print(f"File '{file_name}' not found.")
        elif command.startswith('download '):
            file_name = command.split(' ', 1)[1]
            with open(file_name, 'wb') as f:
                file_data = client.recv(4096)
                f.write(file_data)
            print(f"File '{file_name}' downloaded.")
        else:
            response = client.recv(4096).decode('utf-8')
            print(response)

if __name__ == "__main__":
    connect_to_server()

