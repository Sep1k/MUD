import winsound
from tkinter import *
import subprocess
import sys


# Function to play the sound in a separate thread
try:
    while True:  # Loop for playing music infinitely
        winsound.PlaySound('Ambient.wav', winsound.SND_FILENAME)
except:
    pass


root = Tk()
root.configure(bg="black")

# Scrollbar for both text widgets
scrollbar = Scrollbar(root, bg="gray")
scrollbar.pack(side=RIGHT, fill=Y)

# First Text widget for displaying ASCII logo (disabled for input)
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
                        //" |]     ¤0¤     ||          @==""´´             ´´´´´´´´        
                       %|   [|      "     /%                                         
                       {|    \\\_         //                                           
                       ||      \\\______/% \\\                                               
                       \\\_      '------´   \\\                                 
                        ""+_/|             |>                                      
                             \\\_   !|     //                                      
                               \\\_%/ \_ _%"                                      
                                 "     ""                                         
'''

# Text widget for the ASCII logo
logo_text = Text(root, height=27, width=100, yscrollcommand=scrollbar.set, bg="black", fg="white", wrap=WORD)
logo_text.insert(END, logo_art)
logo_text.config(state=DISABLED)  # Disable editing for the ASCII logo
logo_text.pack()

# Second Text widget for user input
input_text = Text(root, height=10, width=100, yscrollcommand=scrollbar.set, bg="black", fg="white", wrap=WORD)
input_text.pack()

# Configure scrollbar for both Text widgets
scrollbar.config(command=input_text.yview)

def on_mouse_wheel(event):  # Working scrollwheel in game
    input_text.yview_scroll(int(-1*(event.delta/120)), "units")
    logo_text.yview_scroll(int(-1*(event.delta/120)), "units")  # Allow scrolling in both text widgets

root.bind_all("<MouseWheel>", on_mouse_wheel)

last_data = logo_art  # Start with the logo art in last_data for capturing user input after that

def capture_enter(event):
    global last_data
    current_data = input_text.get("1.0", END).strip()  # Get the current content of the user input Text widget

    # Find the new data by subtracting last captured data
    new_data = current_data[len(last_data):].strip()

    if new_data:  # Only print new data if it exists
        print("New data captured:", new_data)
        last_data = current_data  # Update last_data to the current data
        if new_data == "asd":
            print("saadi kätte asd")
        if new_data == "host":
            subprocess.run("server.py")
            sys.exit()

input_text.bind("<Return>", capture_enter)

mainloop()
