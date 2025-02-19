import winsound
from tkinter import *
import subprocess
import sys

try:  # Laulu mängimine igavesti
    while True:
        winsound.PlaySound('Ambient.wav', winsound.SND_FILENAME)
except:
    pass

root = Tk()  # Akna tegemine

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
    global last_data, logo_art
    current_data = input_text.get("1.0", END).strip() # võtab kirjutatud lõigu
    
    
    if current_data:
        print("New data captured:", current_data)
        
        logo_art += "\n" + current_data
        
        logo_text.config(state=NORMAL)  
        logo_text.delete(1.0, END)
        logo_text.insert(END, logo_art) 
        logo_text.config(state=DISABLED)  

        logo_text.see(END)

        
        if "help" in current_data:
            print("saadi kätte abikutse")
        if "host" in current_data:
            subprocess.run(["python", "server.py" ])
            
            sys.exit()
        if "join" in current_data:
            subprocess.run(["python", "client.py"])
            
            sys.exit()

    current_data = ""
input_text.bind("<Return>", capture_enter)

mainloop()
