import winsound
from tkinter import *
import socket
import subprocess
import re
import random
import time
import threading
import os


name = ""
hostname = socket.gethostname()
ip =  socket.gethostbyname(hostname)
port = ""
print(ip)
data = "ase"

def play_music_looped(stop_event):
    sound_file = 'filaes/sounter/ambient.wav'
    if not os.path.exists(sound_file):
        print(f"Error: Sound file not found at {os.path.abspath(sound_file)}")
        return

    print(f"Starting looped background music: {os.path.abspath(sound_file)}")
    try:
        # Play asynchronously and loop
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP | winsound.SND_NODEFAULT)

        # Keep the thread alive while the stop event isn't set
        stop_event.wait() # This will block until stop_event.set() is called

        # Stop the sound when the event is set
        print("Stopping background music.")
        winsound.PlaySound(None, winsound.SND_PURGE)

    except Exception as e:
        print(f"Error starting/playing looped sound: {e}")

#def play_music(stop_event): #play music with threading
#   while not stop_event.is_set():
#       winsound.PlaySound('filaes/sounter/ambient.wav', winsound.SND_FILENAME)
#       time.sleep(100)  

#stop_event = threading.Event()

#music_thread = threading.Thread(target=play_music, args=(stop_event,))
#usic_thread.daemon = True  
#music_thread.start()

gamestate = 0 


root = Tk()  # Akna tegemine

root.title("MUD Chiclantis")
icon = PhotoImage(file='filaes/gameicon.png')
root.iconphoto(True, icon)

# Scrollbar
scrollbar = Scrollbar(root, bg="black", troughcolor="black", highlightbackground="black", highlightcolor="black")
scrollbar.pack(side=RIGHT, fill=Y)

logo_art = '''                      ||       ||                                      |__|_       |________________
                      ||_______||                                     /000000\ 
                ___--%==========%=---_                                |0000000\ 
             _--""                   \\\_             _______         <|000}  ""         
          _//                          |-           |_______|         |0_0¤     
        _//                              \\\                            "¤"     _____________________ 
       //              ____                \\\           ______________________|_____________________                          
      ||         _----4"  ""--__            [|         |                        
     //        _//"""           \\\           |]        |    ##\      ##\ ##\   ##\ #######\                                   
    ||       _//                ||           ||        |    ###\    ### |## |  ## |##  __##\                                 
   ||      _/%        _____    //            |!        |    ####\  #### |## |  ## |## |  ## | 
   ||___--__-----""""     ||  //            [|         |    ##\##\## ## |## |  ## |## |  ## |
  /--""                    ||               [|         |    ## \###  ## |## |  ## |## |  ## |        
 "                          }]             {{          |    ## |\#  /## |## |  ## |## |  ## |                         
                           [|              ||_____ -   |    ## | \_/ ## |\######  |#######  /  
                           ||       _      |/-   _"/   |    \__|     \__| \______/ \_______/ 
                          _[|      00¤     ||--""      |     Chiklantis
                        //" |]     ¤0¤     ||         _|____________________________________________
                       %|   [|      "     /%         | Type host or join to start the game.                           
_                      {|    \\\_         //          |______________________________________________                               
_|                       ||      \\\______/% \\\                             |________________________                 
         _____         \\\_      '------´   \\\                       __               |______________
        |_____|          ""+_/|             |>                      |__|                
                             \\\_   !|     //                                       _________________
______                         \\\_%/ \_ _%"                                       |_________________
______|___________________       "     ""  
__________________________|                                                                         
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
luba_cliendil_jätkata = 0
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------




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
    print("check_server")
    global gamestate, data, luba_cliendil_jätkata
    luba_cliendil_jätkata = 0
    if gamestate == 6:

        return  # Game has started, no need to check server anymore
    else:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)  # Timeout to prevent infinite waiting
            client_socket.connect((joined_ip, int(joined_port)))  # Use actual IP and port
            client_socket.sendall("Kas mäng on alanud liitunud????".encode('utf-8'))
            
            data = client_socket.recv(4096).decode('utf-8')  # Receive data and decode
            print(f"Received data: {data}")  # For debugging
            
            if data:
                if data == "Mäng on alanud!!!!!":  # Make sure the server responds correctly
                    logo_text.config(state=NORMAL)
                    logo_text.delete("1.0", END)
                    logo_art = "Game has started. type help for help! Go win!!!"
                    logo_text.insert(END, logo_art)
                    logo_text.config(state=DISABLED)
                    logo_text.see(END)
                    input_text.delete("1.0", END)
                    gamestate = 6
                    luba_cliendil_jätkata = 0
                else:
                    print(f"Unexpected server response: {data}")
            else:
                print("No data received from the server, retrying...")
        except Exception as e:
            print(f"Error while checking server: {e}")

        # Retry after 1000 ms if the game hasn't started
        root.after(1000, check_server)





def nime_panemine_c():
    global gamestate, data, client_socket, name
    print("siin on nimi mis saadetaks kohe serverile.", name)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    saadetis = f"nameisindata {name}"
    if saadetis == "nameisindata" and saadetis == "nameisindata ":
        print("nimi on tühi")
        logo_text.config(state=NORMAL)
        logo_text.delete("1.0", END)
        logo_art += (str("\ninvalid name. Try again"))
        logo_text.insert(END, logo_art)
        logo_text.config(state=DISABLED)
        logo_text.see(END)
        input_text.delete("1.0", END)
        return
    print("nimi mille saatis client serverile", saadetis)
    client_socket.connect((joined_ip, int(joined_port)))
    client_socket.sendall(saadetis.encode('utf-8'))
    data = client_socket.recv(1024)
    
    # client_socket.close()
    print(data)
    print("saavutasin ühenduse serveriga saates nime")
    
    
    if data == b"nimi on saadaval":
        gamestate = 6
        print(name)
        print(f"Server alustas mängu {data.decode('utf-8')}")
        
        try:
            logo_text.config(state=NORMAL)
            logo_text.delete("1.0", END)
            logo_art = (str("Waiting for game to start"))
            logo_text.insert(END, logo_art)
            logo_text.config(state=DISABLED)
            logo_text.see(END)
            input_text.delete("1.0", END)
            logo_text.config(state=Tk.DISABLED)
            # Use after() to simulate a delay before continuing with the next step
            #def delayed_disable():
            #    try:
            #        logo_text.config(state=Tk.DISABLED)
            #    except:
            #        pass
            # Schedule delayed_disable() to be called after 3 seconds (3000ms)
            #root.after(3000, delayed_disable())
        except:
            print("tekib viga gamestate 5")
    elif data == "nimi ei ole saadaval":
        print("Lühkusin end ära siin ")
        logo_text.config(state=NORMAL)
        logo_text.delete("1.0", END)
        logo_art += (str("\ninvalid name. Try again"))
        logo_text.insert(END, logo_art)
        logo_text.config(state=DISABLED)
        logo_text.see(END)
        input_text.delete("1.0", END)
        
        return



















def capture_enter(event):
    global last_data, logo_art, root, ip, port, gamestate, joined_ip, joined_port, data, name
    if luba_cliendil_jätkata == 1:
        print("Ei ole lubatud jätkata")
        return
    print(gamestate)
    current_data = input_text.get("1.0", END).strip() # võtab kirjutatud lõigu
   

    try:
        number = random.randint(3, 4)  # 1 ja 5 on väga kehvasti kuulda. 2 on kehvasti kuulda
        pop_sound = str("filaes/sounter/" + "pop" + str(number) + ".wav")  # Convert the number to a string
        winsound.PlaySound(pop_sound, winsound.SND_FILENAME)
        print(pop_sound)
    except:
        print(f"Error related to pop sound (even if commented out): {e}")
        pass    
    current_data = current_data.lower()
    current_data.lower
    print(current_data)
    if gamestate == 6: # main küsimine sealt serverilt 
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
            file.write(f"{name} põld 200 \n")
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
            print(f"Serverile ei jõudnud nimi kohale 234")
            print(e)

        finally:
            client_socket.close()
            print("keegi ei tea mu nime ", port)
            

        


    if gamestate == 5: # nime panemine mängijale.
        name = current_data
        name += ""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            
            
            
            nime_panemine_c()
            
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
