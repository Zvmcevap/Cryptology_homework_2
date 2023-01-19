import tkinter
from tkinter import *
from tkinter import ttk


class Letter:
    def __init__(self, original):
        self.original = original
        self.substitute = None
        self.has_been_replaced = False


class GUI:
    def __init__(self, text):
        self.root = Tk()
        self.root.geometry("1500x700")
        self.root.title("Substitucija")

        self.crypto_text = text
        self.tk_crypto_text = None
        self.decrypted_text = text.lower()
        self.tk_decrypto_text = None

        self.alphabet = list("ABCČDEFGHIJKLMNOPRSŠTUVZŽ")
        self.substitutions = [Letter(original=letter) for letter in self.alphabet]
        # Tkinter ni zabaven
        self.tk_substitution_entries = {}

        self.single_letters = None
        self.short_words = None

        self.add_initial_text()
        self.init_statical_fields()
        self.init_substitution_field()

    def add_initial_text(self):
        title = ttk.Label(self.root, text="DeFIŠrator", font=("Ariel", 20))
        title.pack(side=TOP, pady=20)

        text_frame = Frame(self.root)

        crypto_frame = ttk.Labelframe(text_frame, text="Original Besedilo")
        crypto_frame.grid(row=0, column=0, ipadx=10, ipady=10)
        self.tk_crypto_text = tkinter.Text(crypto_frame, height=10, wrap="word")
        self.tk_crypto_text.insert(END, self.crypto_text)
        self.tk_crypto_text.pack()

        decrypted_frame = ttk.Labelframe(text_frame, text="Spremenjeno Besedilo")
        decrypted_frame.grid(row=0, column=1, ipadx=10, ipady=10)
        self.tk_decrypto_text = Text(decrypted_frame, height=10, wrap="word")
        self.tk_decrypto_text.pack()
        self.write_text()
        self.tk_decrypto_text["state"] = "disabled"
        text_frame.pack()

    def init_statical_fields(self):
        stat_frame = ttk.Labelframe(self.root, text="Statistika", padding=10)
        stat_frame.pack(expand=True)

        self.single_letters = ttk.Labelframe(stat_frame, text="Posamezne Črke", padding=5)
        self.single_letters.pack(expand=True)

        self.short_words = ttk.Labelframe(stat_frame, text="Male Besede", padding=5)
        self.short_words.pack(expand=True)

    def fill_statistical_fields(self, letters, words):
        sorted_letters = sorted(letters.items(), key=lambda x: x[1], reverse=True)
        for i, letter in enumerate(dict(sorted_letters)):
            ttk.Label(self.single_letters, text=letter).grid(row=0, column=(2 * i), padx=5)
            ttk.Label(self.single_letters, text=str(letters[letter]) + "%").grid(row=1, column=(2 * i), padx=5)
            ttk.Separator(self.single_letters, orient="vertical").grid(column=(2 * i + 1), row=0, rowspan=2,
                                                                       sticky="ns")

        sorted_two_letter_words = sorted(words[0].items(), key=lambda x: x[1], reverse=True)

        for i, word in enumerate(dict(sorted_two_letter_words)):
            ttk.Label(self.short_words, text=word).grid(row=0, column=(2 * i), padx=10)
            ttk.Label(self.short_words, text=str(words[0][word])).grid(row=1, column=(2 * i), padx=10)
            ttk.Separator(self.short_words, orient="vertical").grid(column=(2 * i + 1), row=0, rowspan=2, sticky="ns")

        sorted_three_letter_words = sorted(words[1].items(), key=lambda x: x[1], reverse=True)
        for i, word in enumerate(dict(sorted_three_letter_words)):
            i = i + len(sorted_two_letter_words)
            ttk.Label(self.short_words, text=word).grid(row=0, column=(2 * i), padx=10)
            ttk.Label(self.short_words, text=str(words[1][word])).grid(row=1, column=(2 * i), padx=10)
            ttk.Separator(self.short_words, orient="vertical").grid(column=(2 * i + 1), row=0, rowspan=2, sticky="ns")

    def init_substitution_field(self):
        substitution_frame = ttk.LabelFrame(self.root, text="Substitucije")
        substitution_frame.pack(pady=50, ipady=10)
        for i, letter in enumerate(self.alphabet):
            ttk.Label(substitution_frame, text=letter).grid(row=0, column=(2 * i), padx=5)
            entry = ttk.Entry(substitution_frame, width=2)
            entry.grid(row=1, column=(2 * i), padx=5)
            entry.bind("<KeyRelease>", self.on_letter_change)  # keyup
            self.tk_substitution_entries[entry] = letter
            ttk.Separator(self.single_letters, orient="vertical").grid(column=(2 * i + 1),
                                                                       row=0,
                                                                       rowspan=2,
                                                                       sticky="ns")

    def on_letter_change(self, event):
        entry = event.widget
        original_letter = self.tk_substitution_entries[entry]
        subs_letter = entry.get().upper()

        if len(subs_letter) > 1:
            entry.delete(0, entry.index("end") - 1)
            subs_letter = subs_letter[-1]
        entry.delete(0, END)
        entry.insert(0, subs_letter)
        index_of_letter = self.alphabet.index(original_letter)
        for i, letter in enumerate(self.substitutions):
            if letter.substitute == subs_letter and i != index_of_letter:
                letter.substitute = None
                letter.has_been_replaced = False
                for e in self.tk_substitution_entries:
                    if self.tk_substitution_entries[e] == self.alphabet[i]:
                        e.delete(0, END)
        replacement = self.substitutions[index_of_letter]
        if subs_letter in self.alphabet:
            replacement.substitute = subs_letter
            replacement.has_been_replaced = True
        else:
            replacement.substitute = None
            replacement.has_been_replaced = False
            entry.delete(0, END)

        self.write_text()

    def write_text(self):
        self.tk_decrypto_text["state"] = "normal"
        self.tk_decrypto_text.delete("1.0", END)
        self.tk_decrypto_text.tag_configure("switched", foreground="navy")
        self.tk_decrypto_text.tag_configure("unchanged", foreground="grey")

        self.decrypted_text = ""
        for letter in self.crypto_text:
            letter = letter.upper()
            if letter in self.alphabet:
                index = self.alphabet.index(letter)
                replacement = self.substitutions[index]
                if replacement.has_been_replaced:
                    self.decrypted_text += replacement.substitute
                    self.tk_decrypto_text.insert(END, replacement.substitute, "switched")
                else:
                    self.decrypted_text += letter
                    self.tk_decrypto_text.insert(END, letter.lower(), "unchanged")
            else:
                self.decrypted_text += letter
                self.tk_decrypto_text.insert(END, letter.lower(), "unchanged")

        self.tk_decrypto_text["state"] = "disabled"

    def run(self):
        self.root.mainloop()


class Analyzer:
    def __init__(self):
        self.crypto_text = None
        self.decrypted_text = None
        self.load_crypto_text()

        # Posamezne črke
        self.letter_count = {}
        self.number_of_letters = 0

        # Besede dolžine 2 in 3
        self.all_words = 0
        self.two_letter_words = {}
        self.three_letter_words = {}

        self.get_statistics()

        self.gui = GUI(self.crypto_text)
        self.gui.fill_statistical_fields(letters=self.letter_count,
                                         words=[self.two_letter_words, self.three_letter_words])
        self.gui.write_text()

        # Automatična analiza - Če mi bo kaj pomagalo od Viginerja
        self.letter_frequency = {'A': 10.47, 'B': 1.94, 'C': 0.66, 'Č': 1.48, 'D': 3.39, 'E': 10.71, 'F': 0.11,
                                 'G': 1.64, 'H': 1.05, 'I': 9.04, 'J': 4.67, 'K': 3.7, 'L': 5.27, 'M': 3.3,
                                 'N': 6.33, 'O': 9.08, 'P': 3.37, 'R': 5.01, 'S': 5.05, 'Š': 1.0, 'T': 4.33,
                                 'U': 1.88, 'V': 3.76, 'Z': 2.1, 'Ž': 0.65}
        self.expected_IC = self.get_correlation_index(frequencies=self.letter_frequency)

    def get_correlation_index(self, frequencies):
        correlation_index = 0
        for letter in frequencies:
            correlation_index += (frequencies[letter] / 100) ** 2
        return correlation_index

    def load_crypto_text(self):
        with open("DN2_tajnopis_substitucija.txt") as f:
            text = f.readline()
            self.crypto_text = text
            self.decrypted_text = text

    def get_statistics(self):
        # Pridobi število črk
        for letter in self.crypto_text:
            if letter in list("ABCČDEFGHIJKLMNOPRSŠTUVZŽ"):
                if letter in self.letter_count:
                    self.letter_count[letter] += 1
                    self.number_of_letters += 1
                else:
                    self.letter_count[letter] = 1
                    self.number_of_letters += 1
        # Izračunaj procente črk
        for letter in self.letter_count:
            self.letter_count[letter] = round(self.letter_count[letter] * 100 / self.number_of_letters, 2)

        # Pridobi posamezne besede
        for word in self.crypto_text.replace(",", "").replace(".", "").split():
            if len(word) == 2:
                if word in self.two_letter_words:
                    self.two_letter_words[word] += 1
                    self.all_words += 1
                else:
                    self.two_letter_words[word] = 1
                    self.all_words += 1
            if len(word) == 3:
                if word in self.two_letter_words:
                    self.three_letter_words[word] += 1
                    self.all_words += 1
                else:
                    self.three_letter_words[word] = 1
                    self.all_words += 1

    def auto_correct_substitutions(self):
        # Razporedi po frekvencah, in naredi primerne menjave
        sorted_text_letters = sorted(self.letter_count.items(), key=lambda x: x[1], reverse=True)
        sorted_substitutions = []
        for letter, frequency in sorted_text_letters:
            print(letter, frequency)
            for sub in self.gui.substitutions:
                if letter == sub.original:
                    sorted_substitutions.append(sub)
        # V tekstu ena črka ni prisotna, tako da:
        for sub in self.gui.substitutions:
            if sub not in sorted_substitutions:
                sorted_substitutions.append(sub)
                print(sub.original)
                break
        sorted_frequencies = sorted(self.letter_frequency.items(), key=lambda x: x[1], reverse=True)
        for i, letter in enumerate(sorted_frequencies):
            print(letter, frequency)
            if sorted_substitutions[i].has_been_replaced:
                continue
            if letter[0] != sorted_substitutions[i].original:
                sorted_substitutions[i].substitute = letter[0]
                sorted_substitutions[i].has_been_replaced = True
            else:
                sorted_substitutions[i].substitute = sorted_frequencies[i + 1][0]
                sorted_substitutions[i].has_been_replaced = True
                sorted_substitutions[i + 1].substitute = sorted_frequencies[i][0]
                sorted_substitutions[i + 1].has_been_replaced = True

        # Dodaj v GUI
        for i, entry in enumerate(self.gui.tk_substitution_entries):
            entry.insert(0, self.gui.substitutions[i].substitute)
        self.gui.write_text()



if __name__ == "__main__":
    app = Analyzer()
    app.auto_correct_substitutions()
    app.gui.run()
