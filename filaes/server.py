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
HOST = "192.168.46.46"
PORT = 1234


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
            print(data)
            name = data.split()
            name2 = name[1]
            print(name2)
            with open('filaes/mängijate nimekiri', 'a') as file:
                print("Server: salvestan mängija nime")
                file.write(name2 + " 200" + "\n")
            client_socket.sendall("server sai nime kätte". encode('utf-8'))
        
    client_socket.close()