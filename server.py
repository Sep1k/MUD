import winsound
from tkinter import *
import socket
import subprocess

hostname = socket.gethostname()
ip =  socket.gethostbyname(hostname)
port = ""
print(ip)
try:  # Laulu mängimine igavesti
    while True:
        winsound.PlaySound('Ambient.wav', winsound.SND_FILENAME)
except:
    pass

gamestate = 0 #mainmenu
           #2 host menu
           #3 ready to host (port is set)
           
def Game():
    pass #siia tuleb gameluup. hetkel client nime all
root = Tk()  # Akna tegemine

root.title("MUD Chickantis")
icon = PhotoImage(file='game icon.png')
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

# Enteri peale salvestatakse kirjutuskasti sisu ja tehakse see tühjaks

def capture_enter(event):
    global last_data, logo_art, root, ip, port, gamestate
    current_data = input_text.get("1.0", END).strip() # võtab kirjutatud lõigu
    if gamestate == 2:
        port = current_data
        try:
            if int(port) < 10000 and int(port) > 1000:
                port = current_data
                gamestate = 3
                subprocess.run(['python', 'server.py'])

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

    if current_data:
        print("New data captured:", current_data)
        
        logo_art += "\n" + current_data
        
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
            gamestate = 2 
        if "join" in current_data:
            #join funktion here
            pass
        else:
            input_text.delete("1.0", END)
input_text.bind("<Return>", capture_enter)

mainloop()
