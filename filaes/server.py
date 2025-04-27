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
    

with open('filaes/kalurinimined.txt', 'w') as file:
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


class Item:
    def __init__(self, name: str, nutra: int, aditionalDamage: int):
        self.name = name
        self.nutra = nutra
        self.aditionalDamage = aditionalDamage

class Room:
    def __init__(self, name: str):
        self.name = name
        self.connectedRooms = []
        self.items = []
        self.previousRoom = None
        self.isLast = False


    def addRoomConnection(self, room):
        self.connectedRooms.append(room)
        if not room.isLast:
            room.previousRoom = self
    def getRoomConnections(self):
        return self.connectedRooms
    def getRoomByName(self, name: str):
        for room in self.connectedRooms:
            if room.name == name:
                return room 
    def printConnections(self):
        asi = ""
        for room in self.connectedRooms:
            asi += f" - {room.name}\n"
        return asi

    def addItem(self, item: Item):
        self.items.append(item)

    def getItemInRoomByName(self, itemName: str):
        found = False
        for item in self.items:
            if itemName == item.name:
                found = True
                return item
        if not found: print("No item Found !!!")



class Player:
    def __init__(self, name: str, currentroom: Room):
        self.name = name
        self.currentRoom = currentroom
        self.health = 100
        self.maxHealth = 150
        self.damage = 20
        self.inv = []
        self.isDead = False

    def goToRoom(self, roomToGo: Room):
        self.currentRoom = roomToGo

    def pickup(self, itemToPick: str, roomFromWherePicked: Room):
        self.inv.append(self.currentRoom.getItemInRoomByName(itemToPick))
        for item in roomFromWherePicked.items:
            if item.name == itemToPick:
                roomFromWherePicked.items.remove(item)
                break
    
    def removeItemFromInv(self, itemName: str):
        for item in self.inv:
            if item.name == itemName:
                self.inv.remove(item)

    def addHealth(self, amount: int):
        self.health =  max(0, min(self.health + amount, self.maxHealth))
        
    def printInv(self):
        print("Invetory")
        for item in self.inv:
            print(item)


class Game:
    def __init__(self, superRoom: Room):
        self.players = []
        self.room = superRoom
        self.room.isLast = True

    def resetPlayers(self):
        for i in range(len(self.players)):
            self.players[i] = Player(self.room)
    
    def emptyWorld(self):
        pass #Doto - Ad function to cloar all the rooms and items from the world

    def recRoomHelpper(self, name: str, room: Room):
        for rooma in room.connectedRooms:
            if rooma.name == name:
                return rooma
            else:
                found = self.recRoomHelpper(name, rooma)
                if found: return found
        return None 

    def getRoomByNameFromAll(self, shearchableRoomName: str):
        for room in self.room.connectedRooms:
            if room.name == shearchableRoomName:
                return room
            else:
                found = self.recRoomHelpper(shearchableRoomName, room)
                if found: return found
        return None 

    def command(self, playerName: str, command: str):
        if command == "": #Kui ei command on tühi siis lõppetab
            print("Co Command were given!")
            return
        ina = command.split()
        cplayer = self.getPlayerByName(playerName)
        
        if ina[0] == "msg":
            msg = ""
            for m in ina[1:]:
                msg += f" {m}"
            
            return str(f"{cplayer.name} sayd: {msg}")
        elif ina[0] == "reset-players":
            self.resetPlayers()   
            return str("Players have been reset!")
        
        if cplayer.health <= 0:
            return str("You are dead")
        else:
            if ina[0] == "look":
                asi = (f"You see: \n")
                n = cplayer.currentRoom.printConnections()
                return n
            elif ina[0] == "go":
                gotThrough = False
                asi = ""
                for room in cplayer.currentRoom.connectedRooms:
                    if room.name == ina[1]:
                        gotThrough = True
                        cplayer.goToRoom(room)
                        asi += (f"{cplayer.name} läks {room.name}!\n")
                        
                if gotThrough == False: asi += (f'Pragu nimega "{ina[1]}" ei leitud!')
                return asi
            elif ina[0] == "back":
                if cplayer.currentRoom.previousRoom != None:
                    cplayer.goToRoom(cplayer.currentRoom.previousRoom)
                else: 
                    print("The gate off Hell is closed for you!")
            elif ina[0] == "scan":
                print("In the room are: ")
                for item in cplayer.currentRoom.items:
                    print(f" - {item.name}")

                print("There are also people: ")
                for player in self.players:
                    if self.isPlayerInSameRoom(cplayer, player) and (player.name != cplayer.name):
                        print(f" - {player.name}")
            elif ina[0] == "where":
                roomChain = " <-- You are here!"
                WhereCCR = cplayer.currentRoom
                roomChain = WhereCCR.name + roomChain 
                temp_room = WhereCCR
                while temp_room.previousRoom is not None:
                    temp_room = temp_room.previousRoom
                    roomChain = f"{temp_room.name} --> " + roomChain
                
                print(roomChain)
            elif ina[0] == "pick":
                picked = False
                for item in cplayer.currentRoom.items:
                    if item.name == ina[1]:
                        picked = True
                        print(f"picked up {ina[1]}!")
                        cplayer.pickup(ina[1], cplayer.currentRoom)
                if not picked: print(f"No item found with name: {ina[1]}")
            elif ina[0] == "inv":
                print("Items in pockets:")
                if cplayer.inv:
                    for item in cplayer.inv:
                        print(f" - {item.name}")
                else:
                    print("Nothing")
            elif ina[0] == "eat":
                for item in cplayer.inv:
                    if item.name == ina[1]:
                        if item.nutra != 0:
                            cplayer.removeItemFromInv(ina[1])
                            cplayer.addHealth(item.nutra)
                            print(f"You ate {ina[1]}")
                        else:
                            print("Your mouth doesn't exept it as food!")
            elif ina[0] == "health":
                print(f"You have health of {cplayer.health}")
            elif ina[0] == "hit":
                for player in game.players:
                    if player.name != ina[1]: continue
                    if player.currentRoom == cplayer.currentRoom:
                        damage = cplayer.damage
                        for item in cplayer.inv:
                            damage += item.aditionalDamage
                        player.addHealth(-damage)
                        print(f"Hit player {player.name} for damage of {damage}")
            else:
                print("unknown command")
        
        

    
    def joinPlayer(self, playerName):
        self.players.append(Player(playerName, self.room))

    def getPlayerByName(self, playerName: str):
        for player in self.players:
            if player.name == playerName:
                return player
    
    def isPlayerInSameRoom(self, og: Player, bg:Player):
        if og.currentRoom == bg.currentRoom:
            return True

    def myfunc(self):
        return ("Hello my name is server!")



game = Game(Room("aed"))

def setUpGame(game: Game):
    game.joinPlayer("A")
    game.joinPlayer("B")
    game.room.addRoomConnection(Room("Kelder"))
    game.room.addRoomConnection(Room("Kirik"))
    game.room.addItem(Item("Kepp", 0, 50))
    game.room.addItem(Item("oun", 20, 0))
    game.room.addItem(Item("Liha", -30, 0))
    game.room.addItem(Item("Seppik", 100, 0))

    game.room.getRoomByName("Kirik").addRoomConnection(Room("Torn"))
    game.room.getRoomByName("Kirik").addRoomConnection(Room("Kabel"))

    game.getRoomByNameFromAll("Torn").addRoomConnection(game.room)

    game.getRoomByNameFromAll("Kelder").addRoomConnection(Room("Moosi-purk"))

setUpGame(game)

# def Game_brain(data):
#     global q, Mkorrad
#     data = data.lower()
#     if data in ["tere", "hi", "hello", "you"]:
#         return "Tere"
#     elif data == "map":
#         Mkorrad += 1
#         return f"Mappi on vaadatud {Mkorrad}"
#     elif data == "name":
#         with open('filaes/kalurinimined.txt','r') as file3:
            
#             return file3
#     else:
#         return "Vigane command"

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
        
            saadud_command = data.split(";")
            print("Server:", saadud_command)
            response = str(game.command(saadud_command[0], saadud_command[1]))
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
            name2 = name[1] # Viga tekkis siin !!!! äkki vahetada ära asukoht nameisindata ja nime vahel.
            print(name2)

            

            player_location = "pold"
            with open('filaes/kalurinimined.txt', 'a') as file:
                print("Server: salvestan mängija nime")
                try:
                    with open('filaes/kalurinimined.txt', 'r') as file: 
                        print("Server: Kontrollin mängija nime")
                        if name2 in file:
                            client_socket.sendall("nimi ei ole saadaval".encode('utf-8'))
                            print("SERVER: nimi ei ole saadaval")
                            continue 
                        else:
                            with open('filaes/kalurinimined.txt', 'a') as append_file: 
                                append_file.write(name2 + '\n')
                                client_socket.sendall("nimi on saadaval".encode('utf-8'))
                                game.joinPlayer(name2)
                except FileNotFoundError:
                    with open('filaes/kalurinimined.txt', 'a') as append_file:
                        append_file.write(name2 + '\n') 
                        client_socket.sendall("nimi on saadaval".encode('utf-8'))
                        print("No File found!")
                with open('filaes/kalurinimined.txt', 'w') as file:
                    file.write(str(name2) + " 200 " +  "\n" )
            client_socket.sendall("server sai nime katte".encode('utf-8'))

            

        if data == "Kas mäng on alanud liitunud????":
            if alustatud == 1:
                print("SERVER: saatsin kinnituse")
                client_socket.sendall("Mäng on alanud!!!!!".encode('utf-8'))
    client_socket.close()