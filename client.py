import socket
# suva
SERVER_IP = '172.20.2.26'  # Muuda see serveri tegelikuks IP-aadressiks
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

        # Oodake serveri vastust
        data = client_socket.recv(1024)  # Loe kuni 1024 baiti
        if data:  # Kontrollime, et andmed pole tühjad
            print(f"Vastus serverilt: {data.decode('utf-8')}")
        
    except Exception as e:
        print(f"Tekkis viga: {e}")
    finally:
        client_socket.close()

