import winsound
from tkinter import *
import subprocess
import sys




try:
    while True:#loop for playing music infinit
        winsound.PlaySound('Ambient.wav', winsound.SND_FILENAME) #starts playing music
except: 
    pass




root = Tk()
root.configure(bg="black")

scrollbar = Scrollbar(root, bg="gray")
scrollbar.pack(side=RIGHT, fill=Y)

mylist = Listbox(root, yscrollcommand=scrollbar.set, bg="black")

T = Text(root, height=30, width=90, yscrollcommand=scrollbar.set, bg="black", fg="white")
T.pack()
T.insert(END, 'Type "help" for help.\nType "host" to host the game.\nType "join" to join the game.\n')

scrollbar.config(command=T.yview,)

def on_mouse_wheel(event): #working scrollwheel in game
    T.yview_scroll(int(-1*(event.delta/120)), "units")

T.bind_all("<MouseWheel>", on_mouse_wheel,)

last_data = 'Type "help" for help.\nType "host" to host the game.\nType "join" to join the game.\n'

def capture_enter(event):
    global last_data
    current_data = T.get("1.0", END).strip()  # Get the current content of the Text widget

    # Find the new data by subtracting last captured data
    new_data = current_data[len(last_data):].strip()
    
    if new_data:  # Only print new data if it exists
        print("New data captured:", new_data)
        last_data = current_data  # Update last_data to the current data
        if new_data == "asd":
            print("saadi kätte asd")
        if new_data == ("host"):
            subprocess.run("server.py")
            sys.exit()
T.bind("<Return>", capture_enter)



mainloop()
