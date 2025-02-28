import winsound
from tkinter import *
import socket
import subprocess
import re

hostname = socket.gethostname()
ip =  socket.gethostbyname(hostname)
port = ""
print(ip)
#try:  # Laulu mängimine igavesti
#    while True:
#        winsound.PlaySound('filaes/Ambient.wav', winsound.SND_FILENAME)
#except:
#    pass

gamestate = 0 #mainmenu
           #2 host menu
           #3 join enter ip
           #4 join enter port
           


root = Tk()  # Akna tegemine

root.title("MUD Chickantis")
icon = PhotoImage(file='filaes/gameicon.png')
root.iconphoto(True, icon)

# Scrollbar
scrollbar = Scrollbar(root, bg="black", troughcolor="black", highlightbackground="black", highlightcolor="black")
scrollbar.pack(side=RIGHT, fill=Y)

logo_art = '''                      ||       ||                                      |__|_   
                      ||_______||                                     /000000\ 
                ___--%==========%=---_                                |0000000\ 
             _--""                   \\\_                             <|000}  ""         
          _//                          |-                             |0_0¤     
        _//                              \\\                            "¤"      
       //              ____                \\\                                   
      ||         _----4"  ""--__            [|                                  
     //        _//"""           \\\           |]                                        
    ||       _//                ||           ||                                        
   ||      _/%        _____    //            |!       @==--……________     _______………………---………………____
   ||___--__-----""""     ||  //            [|          |           ´´´´´´´  
  /--""                    ||               [|          |   Multi User Dungeon                   
 "                          }]             {{            |                          
                           [|              ||_____ -     |                                 
                           ||       _      |/-   _"/    |   Type host or join to continue     
                          _[|      00¤     ||--""       |     ______________      __________________
                        //" |]     ¤0¤     ||          @==""´´´´´´         ´´´´´´´´        
                       %|   [|      "     /%                                         
                       {|    \\\_         //                                           
                       ||      \\\______/% \\\                                               
                       \\\_      '------´   \\\                                 
                        ""+_/|             |>                                      
                             \\\_   !|     //                                      
                               \\\_%/ \_ _%"                                      
                                 "     ""                                          
'''

# Textboxi tegemine, milles on sees logo.
logo_text = Text(root, height=27, width=100, yscrollcommand=scrollbar.set, bg="black", fg="white", wrap=WORD, borderwidth=0)
logo_text.insert(END, logo_art)
logo_text.config(state=DISABLED)
logo_text.pack()

# Kast, mille sisse kasutaja kirjutab
input_text = Text(root, height=1, width=100, yscrollcommand=scrollbar.set, bg="black", fg="white", wrap=WORD, borderwidth=0)
input_text.pack()

scrollbar.config(command=logo_text.yview, bg="black")

# Scrollbari töötamine
def on_mouse_wheel(event):
    logo_text.yview_scroll(int(-1*(event.delta/120)), "units")
    

root.bind_all("<MouseWheel>", on_mouse_wheel)

# Kui hiirt vajutatakse, siis muutub aktiivseks tekstikast.
def on_click(event):
    input_text.focus()
    
root.bind("<Button-1>", on_click)

last_data = ""  
new_data = ""
joined_ip = ""
joined_port = ""
name = ""
def is_valid_ip(ip_str):
    # Regex pattern to match valid IPv4 addresses
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip_str))
# Enteri peale salvestatakse kirjutuskasti sisu ja tehakse see tühjaks

















def capture_enter(event):
    global last_data, logo_art, root, ip, port, gamestate, joined_ip, joined_port
    print(gamestate)
    current_data = input_text.get("1.0", END).strip() # võtab kirjutatud lõigu
   # current_data = str(current_data.lower)
    print(current_data)
    if gamestate == 6: # main küsimine sealt serverilt (mängi ise)
        message = current_data
    
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((joined_ip, joined_port))
            client_socket.sendall(message.encode('utf-8'))
            print("Sõnum saadetud!")

            # Oodake serveri vastust
            data = client_socket.recv(1024)  # Loe kuni 1024 baiti
            if data:  # Kontrollime, et andmed pole tühjad
                logo_art += "\n" + data.decode('utf-8')
        
                logo_text.config(state=NORMAL)  
                logo_text.delete(1.0, END)
                logo_text.insert(END, logo_art) 
                logo_text.config(state=DISABLED)  

                logo_text.see(END)
                print(f"Vastus serverilt: {data.decode('utf-8')}")
            
        except Exception as e:
            print(f"Tekkis viga: {e}")
        finally:
            client_socket.close()
            input_text.delete("1.0", END)

    if gamestate == 7:
        if current_data == "start":
            gamestate == 6
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            client_socket.sendall("siia käib rida, mis käivitab server.".encode('utf-8'))
            data = client_socket.recv(1024)
            gamestate = 6
            if data:
                print(f"Server alustas mängu .{data.decode('utf-8')}")
        except Exception as e:
            print(f"Serveri alustamisega tekjkis viga")
        finally:
            client_socket.close()

    if gamestate == 8:
        name = current_data
        name += ""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            client_socket.sendall(name.encode('utf-8'))
            data = client_socket.recv(1024)
            gamestate = 6
            if data:
                print(f"Server alustas mängu .{data.decode('utf-8')}")
        except Exception as e:
            print(f"Serveri alustamisega tekjkis viga")
        finally:
            client_socket.close()
            

        logo_text.config(state=NORMAL)
        logo_text.delete("1.0", END) 
        logo_art = (str("Ready to Game\n"  "Type help for help"))
        logo_text.insert(END, logo_art)
        logo_text.config(state=DISABLED)
        logo_text.see(END)
        input_text.delete("1.0", END)
        gamestate = 7


    if gamestate == 5: # nime panemine mängijale.
        name = current_data
        name += ""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file.w
            

        logo_text.config(state=NORMAL)
        logo_text.delete("1.0", END) 
        logo_art = (str("Ready to Game\n"  "Type help for help"))
        logo_text.insert(END, logo_art)
        logo_text.config(state=DISABLED)
        logo_text.see(END)
        input_text.delete("1.0", END)
        gamestate = 6


    if gamestate == 4:
        joined_port == current_data
        try:
            if int(port) < 10000 and int(port) > 1000:

                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END) 
                logo_art = (str("Enter name:"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)

                gamestate = 5
                logo_art.delete("1.0", END)
                return
            else:
                logo_text.config(state=NORMAL)  
                logo_text.delete(1.0, END)
                logo_art += "\nPort is invalid. \nTry again."
                logo_text.insert(END, logo_art) 
                logo_text.config(state=DISABLED)
                input_text.delete("1.0", END)
                return
        except:
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_art += "\nPort is invalid. \nTry again."
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)
            input_text.delete("1.0", END)
            return
        
        print(joined_port)


    if gamestate == 3:
        joined_ip = current_data
        try:
            print('aaaa', joined_ip)
            if is_valid_ip(joined_ip):
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END) 
                logo_art = (str("Joining Game\n IP = " + joined_ip + "\nEnter PORT you want to join:"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)

                gamestate = 4
                
                return

            else:
                logo_text.config(state=NORMAL)  
                logo_text.delete(1.0, END)
                logo_art += "\nIP is invalid. \nTry again."
                logo_text.insert(END, logo_art) 
                logo_text.config(state=DISABLED)
                input_text.delete("1.0", END)
                return
        except:
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_art += "\nIP is invalid. \nTry again."
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)
            input_text.delete("1.0", END)
            return
        

    if gamestate == 2:
        port = current_data
        
        if int(port) > 999 and int(port) < 100000:
            port = current_data
            with open('filaes/kaluriped.txt', 'w') as file: 
                pass #millegipärast kui fail kirjutamiseks avada ja sinna mitte midagi kirjutada kustutatakse selle sisu.
            with open('filaes/kaluriped.txt', 'w') as file:
                file.write(ip + "\n" + port)
            logo_text.config(state=NORMAL)
            logo_text.delete("1.0", END) 
            logo_art = (str("Enter user name"))
            logo_text.insert(END, logo_art)
            logo_text.config(state=DISABLED)
            logo_text.see(END)
            input_text.delete("1.0", END)
            try:
                subprocess.Popen(['python', 'filaes/server.py'])
            except:
                pass
            gamestate = 8

        else:
            print("siin")
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_art += "\nPort is invalid. \nTry again."
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)
            input_text.delete("1.0", END)
            return

           
    if gamestate == 0:   
        if current_data:
            print("New data captured:", current_data)
            
            logo_art += str("\n" + str(current_data))
            
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)  

            logo_text.see(END)

            
            if "help" in current_data:
                print("Help command received")

                input_text.delete("1.0", END)
                help_text = "1. To join a game, type 'join' and press enter.\n2. To host the game, type 'host' and press enter."
                logo_art += "\n" + help_text
                logo_text.config(state=NORMAL)
                logo_text.insert(END, "\n" + help_text) 
                logo_text.config(state=DISABLED)
                logo_text.see(END)
            if "host" in current_data:
                print("User tryed hosting.")
                
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END) 
                logo_art = (str("HOSTING GAME\n IP = " + ip + "\nType in port for game to host on(4 didget number):"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)
                input_text.delete("1.0", END)
                gamestate = 2 
            if "join" in current_data:
                print("user tryed to join")
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END) 
                logo_art = (str("JOINING GAME\nEnter ip address to you want to join:"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)
                input_text.delete("1.0", END)
                gamestate = 3
                
            else:
                input_text.delete("1.0", END)
input_text.bind("<Return>", capture_enter)

mainloop()
