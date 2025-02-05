import socket

HOST = '0.0.0.0'  # Kuulab kõiki võrguadaptereid
PORT = 12345      # Port, mida kuulatakse

# Loo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Lubab kuni 5 ühendust järjekorras

print(f"Server kuulab {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Ühendus: {addr}")

    data = client_socket.recv(1024)  # Loe kuni 1024 baiti
    if data:
        print(f"Sõnum: {data.decode('utf-8')}")

    client_socket.close()
