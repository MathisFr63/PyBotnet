#!/usr/bin/env python3

from platform import system as platform

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

def show_key(event, f):
    if event.keysym == 'Escape':
        root.destroy()
    else:
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == "Return" or event.keysym == "BackSpace":
                print(event.keysym)
                txt = event.keysym
            else:
                print(event.char)
                txt = event.char
        else:
            print(event.keysym)
            txt = event.keysym
        f.write(txt)

output = open(".out.txt", "w")
     
root = tk.Tk() 
root.bind_all('<Key>', lambda event: show_key(event, output))

# Permet de mettre la fenêtre en premier plan sur Mac
if platform() == 'Darwin':      # How Mac OS X is identified by Python
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')  
              
              
print("En écoute (Echap pour quitter)")

root.mainloop()
output.close()
