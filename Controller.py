import socket
import threading
import os
import webbrowser

def handle_client(client_socket):
    while True:
        # Receive command from the client
        command = client_socket.recv(1024).decode('utf-8')
        if not command:
            break
        
        # Process command and generate output
        if command == 'pwd':
            output = os.getcwd()
        elif command.startswith('cd '):
            try:
                os.chdir(command[3:])
                output = os.getcwd()
            except FileNotFoundError as e:
                output = str(e)
        elif command == 'ls':
            output = '\n'.join(os.listdir())
        elif command.startswith('upload '):
            file_data = client_socket.recv(4096)
            file_name = command.split(' ', 1)[1]
            with open(file_name, 'wb') as f:
                f.write(file_data)
            output = f"File uploaded: {file_name}"
        elif command.startswith('download '):
            file_name = command.split(' ', 1)[1]
            if os.path.exists(file_name):
                with open(file_name, 'rb') as f:
                    file_data = f.read()
                client_socket.sendall(file_data)
                output = f"File downloaded: {file_name}"
            else:
                output = f"File not found: {file_name}"
        elif command.startswith('delete '):
            file_name = command.split(' ', 1)[1]
            try:
                os.remove(file_name)
                output = f"File deleted: {file_name}"
            except FileNotFoundError as e:
                output = str(e)
        elif command.startswith('redirect '):
            url = command.split(' ', 1)[1]
            webbrowser.open(url)
            output = f"Redirected to {url}"
        elif command.startswith('fake_error '):
            error_message = command.split(' ', 1)[1]
            output = f"Fake error: {error_message}"
        elif command == 'rickroll':
            webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            output = "Rickrolled!"
        elif command.startswith('cache '):
            # Simulate cache manipulation (could be replaced with actual cache operations)
            output = "Cache manipulated (simulation)"
        else:
            output = "Unknown command"
        
        client_socket.send(output.encode('utf-8'))
    
    client_socket.close()

def start_server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f'Server listening on {host}:{port}')
    
    while True:
        client_socket, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
