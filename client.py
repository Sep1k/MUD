import socket

SERVER_IP = '192.168.1.112'  # Muuda see serveri tegelikuks IP-aadressiks
PORT = 12345

while True:
    message = input("Sisesta sõnum (või 'exit' lõpetamiseks): ")
    
    if message.lower() == 'exit':
        print("Lõpetan programmi.")
        break
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, PORT))
        client_socket.sendall(message.encode('utf-8'))
        print("Sõnum saadetud!")
    except Exception as e:
        print(f"Tekkis viga: {e}")
    finally:
        client_socket.close()

