import tkinter as tk
import string


lower = list(string.ascii_lowercase)
upper = list(string.ascii_uppercase)
numb = list(string.digits)
pun = list(string.punctuation)
pun.append(" ")

symbols = [lower, upper, numb, pun]


class Gui:
    # Masta window and variables
    def __init__(self, master, sym):
        self.master = master  # Najprej defineri masterja in ostale podane argumente
        self.symbols = sym  # -||-
        # Centreri na sredino če nočš fullscreen
        screen_w, screen_h = master.winfo_screenwidth(), master.winfo_screenheight()
        w, h = 1000, 700
        x, y = (screen_w//2) - (w//2), (screen_h//2) - (h//2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master.configure(bg="white")
        self.master.title("Benigma und Buring Maschine")

        # Mal sm še spremenu barve - men je lepš tkole :P

        self.orgtext = ""
        self.enctext = ""
        self.shift = tk.IntVar()  # Tuki nisi rabu dat (), ker je nisi nikoli uporabu - zato ker si self.shift prepisal
        # v funkciji encode() al pa decode() z nekim integerjem - shift si pa dubu s self.scale.get().
        # Namesto tega daš self.shift.get() če že maš v self.scale definirano kot "variable=self.shift)
        self.checkvar = tk.IntVar(value=1)  # Tega nism vedu, da loh daš v oklepaj "value=1". Jst sm zmeri delu
        # na tak način "self.checkvar.set(True)"

        # Frames
        self.frame_top = tk.Frame(self.master, bg="white")
        self.frame_top.pack(fill=tk.BOTH, side=tk.TOP)
        self.frame_but = tk.Frame(self.master, bg="white")
        self.frame_org = tk.LabelFrame(self.master, text="Original message", bg="white")
        self.frame_sol = tk.LabelFrame(self.master, text="Coded message", bg="white")

        self.frame_top.pack(side=tk.TOP)
        self.frame_org.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH, padx=50, pady=40)
        self.frame_but.pack(side=tk.LEFT)
        self.frame_sol.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.BOTH, padx=50, pady=40)

        # Shift scale
        self.scale_frame = tk.LabelFrame(self.frame_but, text="Set shift level", bg="white", bd=0, highlightthickness=0)
        self.scale = tk.Scale(
            self.scale_frame,
            orient=tk.HORIZONTAL,
            length=152,
            from_=0,
            to_=25,
            variable=self.shift,
            command=lambda x: self.encode(),
            bg="white",
            bd=0,
            highlightthickness=0
        )
        self.scale_frame.grid(row=2)
        self.scale.pack()

        # Text boxes
        self.naslov = tk.Label(
                               self.frame_top,
                               text="Benos Enigma and Turing Machine!",
                               font=("", 20),
                               pady=20,
                               padx=10,
                               bg="white"
                               )
        self.naslov.pack()
        self.inputtxtorg = tk.Text(self.frame_org, width=20, height=20, bd=0, highlightthickness=0)
        self.inputtxtorg.pack(expand=tk.TRUE, fill=tk.BOTH)
        self.inputtxtsol = tk.Text(self.frame_sol, width=20, height=20, bd=0, highlightthickness=0)
        self.inputtxtsol.pack(expand=tk.TRUE, fill=tk.BOTH)

        # Buttons
        self.butcode = tk.Button(
                                 self.frame_but,
                                 text="Encode the message\n------->",
                                 fg="red",
                                 width=20,  # V buttonih k spreminjaš napis je fajn dodt fiksn size, da ti ostalim
                                            # widgetom ne spreminja velikosti (textframov v tvojem primeru)
                                 command=lambda: self.encode()
                                 )
        self.butcode.config(activeforeground=self.get_fg())
        self.checkbox = tk.Checkbutton(
            self.frame_but,
            text="Benigma",
            variable=self.checkvar,
            pady=20,
            command=lambda: self.update_check(),
            bd=0,
            bg='white',
            highlightthickness=0,
            activebackground="white"
        )
        self.butcode.grid(row=0)
        self.checkbox.grid(row=1)

        # Ker maš dinamično spreminjanje besed v textframih bi bilo mogoče za razmislt a sploh rabš še un button?
        # Mogoče bi bla funkcija buttona bolša da bi naredu "clear screen" in zbrisu text iz textframov.
        # Puščico pa loh zamenjaš s dejanskimi slikami puščic?

    def get_fg(self):
        fg = self.butcode["fg"]
        return fg

    # Fun in functions
    def update_check(self):
        if self.checkvar.get() == 1:
            self.checkbox.configure(text="Benigma")
            self.butcode.configure(text="Encode the message\n------->", fg="red", activeforeground="red")
        else:
            self.butcode.configure(text="Decode the message\n<------", fg="black", activeforeground="black")
            self.checkbox.configure(text="Buring")

    # Vn sm vrgu decode ker se mi zdi da bi blo lepš tkole... mal mn redundančnosti če ne druzga
    def encode(self):
        benigma = self.checkvar.get()
        shift = self.shift.get()
        if benigma:
            text = self.inputtxtorg.get(1.0, tk.END)
            self.orgtext = text
            self.enctext = ""
        else:
            text = self.inputtxtsol.get(1.0, tk.END)
            self.enctext = text
            self.orgtext = ""
            shift = -shift
        for letter in text:
            for s in self.symbols:
                if letter in s:
                    fpos = s.index(letter)
                    newpos = fpos + shift
                    if benigma:
                        while newpos >= len(s):
                            newpos -= len(s)
                        self.enctext += s[newpos]
                    else:
                        while newpos < 0:
                            newpos += len(s)
                        self.orgtext += s[newpos]
        if benigma:
            self.inputtxtsol.delete(1.0, tk.END)
            self.inputtxtsol.insert(tk.END, self.enctext)
        else:
            self.inputtxtorg.delete(1.0, tk.END)
            self.inputtxtorg.insert(tk.END, self.orgtext)


def main():
    root = tk.Tk()
    Gui(root, symbols)
    root.mainloop()


if __name__ == '__main__':
    main()