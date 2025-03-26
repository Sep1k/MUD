import socket
import random 

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


mapik = random.randint(1,3)
print(mapik)
map = "map"
if mapik == 1:
    map = '''                                  _______Veski                      
                                              /                        
                                             /                         
                                 ____       |                          
                      ___Tiik___/    \__   /                           
                   __/     \__          Põld         Kirik ___         
                  /           \_      _/    \           |     \__Kelder
              Saun              \    /       |           \             
              |            _______Aas _       \           |            
       Leiliruum       __/      /   |  \_      |          |            
                   Laut        /    |    \__   \    __Surnuaed         
                              |      \       Mets__/                   
                             /        |                                
                        __Maja        Koobas                           
            Pööning____/                                               
'''
elif mapik == 2:
    map = '''                            _____Päästekapsel2   
                                  /                     
                                 /    Päästekapsel1     
                                 |   /                  
                         _____   |__/                   
                        /     \_|   |                   
                  Jõusaal       |   |    söökla         
                                |   |___/   \           
                                | K |        \          
                  Magala4_______| O |         \         
                                | R |____     |         
                                | I |    \___Köök       
                  Magala3_______| D |                   
                                | O |____Haigla         
                                | R |                   
                  Magala2_______|   |     ___Mootoriruum
                                |   |____/         /    
                                |___|             /     
                  Magala1_______/   \            /      
                                     \          /       
                                      \__Juhtruum             '''
    

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
alustatud = 0
def Game_brain(data):
    global q, Mkorrad
    data = data.lower()
    if data in ["tere", "hi", "hello", "you"]:
        return "Tere"
    elif data == "map":
        Mkorrad += 1
        return f"Mappi on vaadatud {Mkorrad}"
    elif data == "name":
        with open('filaes/mängijate nimekiri','r') as file3:
            
            return file3
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
            alustatud = 1
            print("Server: alustan mängu")
            client_socket.sendall("Server started".encode('utf-8'))

        elif "nameisindata" in data:
            print("SERVER: Kontrollin nime")
            print(data)
            name = data.split()
            name2 = name[1]
            print(name2)


            player_location = "pold"
            with open('filaes/mängijate nimekiri', 'a') as file:
                print("Server: salvestan mängija nime")
                try:
                    with open('filaes/mängijate nimekiri', 'r') as file: 
                        print("Server: Kontrollin mängija nime")
                        if name2 in file:
                            client_socket.sendall("nimi ei ole saadaval".encode('utf-8'))
                            print("SERVER: nimi ei ole saadaval")
                            continue 
                        else:
                            with open('filaes/mängijate nimekiri', 'a') as append_file: 
                                append_file.write(name2 + '\n') 
                                print("Server: salvestan mängija nime")
                                client_socket.sendall("nimi on saadaval".encode('utf-8'))
                except FileNotFoundError:
                    with open('filaes/mängijate nimekiri', 'a') as append_file:
                        append_file.write(name2 + '\n') 
                        client_socket.sendall("nimi on saadaval".encode('utf-8'))
                with open('filaes/mängijate nimekiri', 'w') as file:
                    file.write(str(name2) + " 200 " +  "\n" )
            client_socket.sendall("server sai nime katte".encode('utf-8'))
        if data == "Kas mäng on alanud liitunud????":
            if alustatud == 1:
                print("SERVER: saatsin kinnituse")
                client_socket.sendall("Mäng on alanud!!!!!".encode('utf-8'))
    client_socket.close()