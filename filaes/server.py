import socket

print("Server proge alustas")

hort = []
print("Server: Serrveri pordi loop ")
with open('filaes/kaluriped.txt', 'r') as file:
    for rida in file:
        print(rida)
        hort.append(rida.strip())

HOST = hort[0]
PORT = int(hort[1])
print("port", PORT)

with open('filaes/mängijate nimekiri', 'w') as file:
    pass
    print("Server: salvestan_mängija nime")
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server kuulab {HOST}:{PORT}")

q = "hello"
Mkorrad = 0
gamestatus = 0
mängijate_arv = 0
players = []

def Game_brain(data):
    global q, Mkorrad
    data = data.lower()
    if data in ["tere", "hi", "hello", "you"]:
        return "Tere"
    elif data == "map":
        Mkorrad += 1
        return f"Mappi on vaadatud {Mkorrad}"
    else:
        return "Vigane command"

def game_status():
    return "Game has started!" if gamestatus == 1 else "Game has not started yet."

while True:
    client_socket, addr = server_socket.accept()
    print(f"Ühendus: {addr}")
    print("server: serverühendus edukalt")
    data = client_socket.recv(2048)
    
    if data:
        data = data.decode('utf-8').strip()
        print("SERVER: ", data)
        print("gamestatus", gamestatus)
        
        if int(gamestatus) == 2:
            print("server: " + f"Sõnum: {data}")
            response = Game_brain(data)
            client_socket.sendall(response.encode('utf-8'))

        elif data == "siia käib rida, mis käivitab server.":
            gamestatus = 2
            print("Server: alustan mängu")
            client_socket.sendall("Server started".encode('utf-8'))

        elif "nameisindata" in data:
            print("SERVER: Kontrollin nime")
            name = data.split()
            name2 = name[1]
            print(name2)

            if gamestatus == 0:
                with open('filaes/mängijate nimekiri', 'a') as file:
                    print("Server: salvestan mängija nime")
                    file.write(name2 + " 200" + "\n")
                    mängijate_arv += 1
                    players.append(name2)
                client_socket.sendall(f"Server sai nime kätte. {mängijate_arv} mängijat on liitunud.".encode('utf-8'))
                print(f"Current number of players: {mängijate_arv}")
            else:
                client_socket.sendall(f"Game already started. {mängijate_arv} players have joined.".encode('utf-8'))

        elif data == "checkstatus":
            current_status = game_status()
            client_socket.sendall(current_status.encode('utf-8'))

    client_socket.close()
