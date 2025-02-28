import socket

print("Server proge alustas")

hort = []
with open('filaes/kaluriped.txt', 'r') as file:
    for rida in file:
        hort.append(rida.strip())

HOST = hort[0]
PORT = int(hort[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server kuulab {HOST}:{PORT}")

q = "hello"
Mkorrad = 0
gamestatus = 0

def Game_brain():
    global q, Mkorrad
    q = q.lower()
    if q in ["tere", "hi", "hello", "you"]:
        return "Tere"
    elif q == "map":
        Mkorrad += 1
        return f"Mappi on vaadatud {Mkorrad}"
    else:
        return "Vigane command"

while True:
    client_socket, addr = server_socket.accept()
    print(f"Ühendus: {addr}")

    data = client_socket.recv(1024)
    if data:
        data = data.decode('utf-8').strip()
        
        if gamestatus == 2:
            print(f"Sõnum: {data}")
            q = data
            response = Game_brain()
            client_socket.sendall(response.encode('utf-8'))

        elif data == "siia käib rida, mis käivitab server.":
            gamestatus = 2
            client_socket.sendall("Server started".encode('utf-8'))

        else:
            with open('fileas/nimekiri mängijatel', 'a') as file:
                file.write("\n" + data)

    client_socket.close()
