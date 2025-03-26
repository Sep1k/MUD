import winsound
from tkinter import *
import socket
import subprocess
import re
import time

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
  /--""                    ||               [|          |   Multi User Dungeon Chickantis                  
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

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Optional: set a timeout of 1 second

    try:
        # Try to connect to the port to see if it's in use
        sock.connect((ip, port))
    except (socket.timeout, socket.error):
        # If there's a timeout or error, the port is available
        return True
    else:
        # If connection is successful, the port is in use
        return False
    finally:
        sock.close()

def check_server():
    if gamestate == 6:

        #viga peitub selle tsükli igaveses jooksmises. tuleb lisada mingi lõpetamise tingimus. ja server saadab kindal stri olenevalt, kas mängija saab liituda.
        try:
            # Siin saad panna oma socketi ühenduse ja vastuvõtu koodi
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)  # Lisame timeout, et vältida lõpmatut ooteaega
            client_socket.connect((joined_ip, int(joined_port)))  # Muuda IP ja port vastavalt
            client_socket.sendall("Kas mäng on alanud liitunud????".encode('utf-8'))
            data = client_socket.recv(4096)
            
            if data:
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END)
                logo_art = "Game has started. type help for help! Go win!!!"
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)
                input_text.delete("1.0", END)
            else:
                # Kui serverilt ei saadud vastust, proovime uuesti
                print("Ei saanud vastust serverilt, proovime uuesti...")
        except Exception as e:
            print(f"Tekkis viga: {e}")

        # Kutsume 'check_server' funktsiooni uuesti 1 sekundi pärast
        root.after(1000, check_server)














def capture_enter(event):
    global last_data, logo_art, root, ip, port, gamestate, joined_ip, joined_port
    print(gamestate)
    current_data = input_text.get("1.0", END).strip() # võtab kirjutatud lõigu
   # current_data = str(current_data.lower)
    current_data.lower
    print(current_data)
    if gamestate == 6: # main küsimine sealt serverilt (mängi ise)
        print("gamestate 6", port)
        print("joined_port: ", joined_port)
        

        current_data = input_text.get("1.0", END).strip()


        if not current_data:
            print("Error: Attempted to send an empty message.")
            return  # If the message is empty, don't proceed

        # Your existing code for constructing message

        message = current_data
        logo_art += str("\n" + str(current_data))
        logo_text.config(state=NORMAL)  
        logo_text.delete(1.0, END)
        logo_text.insert(END, logo_art) 
        logo_text.config(state=DISABLED)  
        logo_text.see(END)

        if current_data == "help":

            logo_art += str("\n" + str(current_data))
            logo_art += "\nCOMMANDS\nmovment\n    go <place>\n    look\n    map\n    touch <itam>\n    scan\nattack\n    shoot <target>\n    weapon\n"
            
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)  
            logo_text.see(END)
            
            
            return
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
           
            
            client_socket.connect((joined_ip, int(joined_port)))
            
            client_socket.sendall(message.encode('utf-8'))
            print("Sõnum saadetud!")

            # Oodake serveri vastust
            data = client_socket.recv(1024)  # Loe kuni 1024 baiti
            print("decoden ja kirjutan serveri saadetis")
            if data:  # Kontrollime, et andmed pole tühjad
                logo_art += "\n" + data.decode('utf-8')
        
                logo_text.config(state=NORMAL)  
                logo_text.delete(1.0, END)
                logo_text.insert(END, logo_art) 
                logo_text.config(state=DISABLED)  

                logo_text.see(END)
                print(f"Vastus serverilt: {data.decode('utf-8')}")
            
        except Exception as e:
            print(f"is viga: {e}")
        finally:
            client_socket.close()
            input_text.delete("1.0", END)

    if gamestate == 7:
        if "start" in current_data:
            gamestate = 6
            
            joined_ip = ip
            joined_port = port
            print(("joind port gs 7 "), joined_port)
        
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_art += "Start is not writen like that."
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)
            input_text.delete("1.0", END)
            print("start input wrong")
            return
        
        try:
            # Ensure port is an integer
            port = int(port)  # This line ensures that port is an integer
            
            print(f"Attempting to connect to {ip}:{port}")
            client_socket.connect((ip, port))  # Connect to server
            print(f"Connected to {ip}:{port}")

            client_socket.sendall("siia käib rida, mis käivitab server.".encode('utf-8'))
            print("Message sent to server.")

            # Wait for response from the server
            data = client_socket.recv(1024)
            if data:
                print(f"Received data from server: {data.decode('utf-8')}")  # Print server response

            # Change gamestate after getting response
            gamestate = 6
            logo_text.config(state=NORMAL)
            logo_text.delete("1.0", END)
            logo_art = (str("Game has begun. Type help for help"))
            logo_text.insert(END, logo_art)
            logo_text.config(state=DISABLED)
            logo_text.see(END)
            input_text.delete("1.0", END)

        except Exception as e:
            print(f"Error starting server: {e}")
            logo_text.config(state=NORMAL)
            logo_text.delete("1.0", END)
            logo_art = (str("There was an error starting the server. \nType start again or fix the error."))
            logo_text.insert(END, logo_art)
            logo_text.config(state=DISABLED)
            logo_text.see(END)
            input_text.delete("1.0", END)

        finally:
            client_socket.close()
            print(port)



    if gamestate == 8:
        name = current_data
        name += ""
        print(name)
        print(port)
        with open('filaes/kalurinimined.txt', 'w') as file: 
            pass #millegipärast kui fail kirjutamiseks avada ja sinna mitte midagi kirjutada kustutatakse selle sisu.
        with open('filaes/kalurinimined.txt', 'w') as file:
            file.write(name)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, int(port)))
            client_socket.sendall(name.encode('utf-8'))
            data = client_socket.recv(1024)
            gamestate = 6
            print("saavutasin ühenduse serveriga saates nime")
            if data:
                print(f"Server alustas mängu .{data.decode('utf-8')}")

            logo_text.config(state=NORMAL)
            logo_text.delete("1.0", END) 
            logo_art = (str("Type start to start the game.\nBe shure that all players have joined."))
            logo_text.insert(END, logo_art)
            logo_text.config(state=DISABLED)
            logo_text.see(END)
            input_text.delete("1.0", END)
            gamestate = 7

        except Exception as e:
            print(f"Serverile ei jõudnud nimi kohale")
            print(e)

        finally:
            client_socket.close()
            print("keegi ei tea mu nime ", port)
            

        


    if gamestate == 5: # nime panemine mängijale.
        name = current_data
        name += ""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            saadetis = f"nameisindata {name}"
            print(saadetis)
            client_socket.connect((joined_ip, int(joined_port)))
            client_socket.sendall(saadetis.encode('utf-8'))
            data = client_socket.recv(1024)
            gamestate = 6
            # client_socket.close()
            print(data)
            print("saavutasin ühenduse serveriga saates nime")
         
            
            if data == b"nimi on saadaval":

                print(f"Server alustas mängu {data.decode('utf-8')}")
                
                try:
                    logo_text.config(state=NORMAL)
                    logo_text.delete("1.0", END)
                    logo_art = (str("Waiting for game to start"))
                    logo_text.insert(END, logo_art)
                    logo_text.config(state=DISABLED)
                    logo_text.see(END)
                    input_text.delete("1.0", END)
                    # Use after() to simulate a delay before continuing with the next step
                    def delayed_disable():
                        try:
                            logo_text.config(state=Tk.DISABLED)
                        except:
                            pass
                    # Schedule delayed_disable() to be called after 3 seconds (3000ms)
                    root.after(3000, delayed_disable)
                except:
                    print("tekib viga gamestate 5")
            elif data == "nimi ei ole saadaval":
                print("L]hkusin end ära siin ")
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END)
                logo_art += (str("\ninvalid name. Try again"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)
                input_text.delete("1.0", END)
                return
            else:
                print("else osa", data)
                print(data)
                print("eelm rida oli data ka")
            print("jõudsin siia")
            
            check_server()
                

        except Exception as e:
            print(f"Serverile ei jõudnud nimi kohale")
            print(e)
            logo_text.config(state=NORMAL)  
            logo_text.delete(1.0, END)
            logo_art += "\nsomething went wrong. Resart program."
            logo_text.insert(END, logo_art) 
            logo_text.config(state=DISABLED)
            input_text.delete("1.0", END)
        finally:
            client_socket.close()
            print("nimi serverile saadetud")





    if gamestate == 4:
        
        port2 = current_data
        try:
            if int(port2) > 999 and int(port2) < 10000:
                joined_port = current_data
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END) 
                logo_art = (str("Enter name:"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)
                gamestate = 5
                input_text.delete("1.0", END)
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



    if gamestate == 3:
        joined_ip = current_data
        print("joined ip = ", joined_ip)
        try:
            print('aaaa', joined_ip)
            if is_valid_ip(joined_ip):
                logo_text.config(state=NORMAL)
                logo_text.delete("1.0", END) 
                logo_art = (str("Joining Game\n IP = " + joined_ip + "\nEnter PORT you want to join:"))
                logo_text.insert(END, logo_art)
                logo_text.config(state=DISABLED)
                logo_text.see(END)
                input_text.delete("1.0", END)
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
        port2 = current_data
        
        try:
            print("port", type(port2), port, int(port2)+1)
            if int(port2) > 999 and int(port2) < 10000:
                print("siia me ei jõua")
                if check_port(int(port2)):
                    print(f"Port {port2} is available.")
                    print("port ei olnud võetud")
                    
                    port = current_data
                    print("siin on port gs2", port)
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
                    print(port)

                else:
                    print(f"Port {port} is already taken.")
                    logo_text.config(state=NORMAL)  
                    logo_text.delete(1.0, END)
                    logo_art += "\nPort is already taken. \nTry other port."
                    logo_text.insert(END, logo_art) 
                    logo_text.config(state=DISABLED)
                    input_text.delete("1.0", END)
                    return

            else:
                print("siin")
                logo_text.config(state=NORMAL)  
                logo_text.delete(1.0, END)
                logo_art += "\nPort is invalid. \nTry again."
                logo_text.insert(END, logo_art) 
                logo_text.config(state=DISABLED)
                input_text.delete("1.0", END)
                return

        except:
            print("siilike")
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
                logo_art = (str("HOSTING GAME\n IP = " + ip + "\nType in port for game to host on(4 didget number)(recomender: 9999):" ))
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
