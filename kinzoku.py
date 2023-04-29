import argparse
import random
import os
import sys
import time
import tkinter as tk

def clrscr() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def gen_addition() -> list:
    num1 = random.randint(1, 999)
    num2 = random.randint(1, 1000 - num1)
    res = num1 + num2
    return [num1, num2, res, "+"]

def gen_subtraction() -> list:
    num1 = random.randint(1, 1000)
    num2 = random.randint(1, num1)
    res = num1 - num2
    return [num1, num2, res, "-"]

def gen_multiplication() -> list:
    num1 = random.randint(2, 100)
    num2 = random.randint(2, 1000 // num1)
    res = num1 * num2
    return [num1, num2, res, "*"]

def gen_division() -> list:
    num2 = random.randint(2, 50)
    num1 = random.choice(list(range(num2, 1000, num2)))
    res = int(num1 / num2)
    return [num1, num2, res, "/"]

def gen_recomms(cor: int) -> str:
    ret = [cor]
    for i in range(4):
        rand = random.randint(cor - 100 if cor > 100 else 1, cor + 100 if cor < 901 else 1000)
        while rand in ret:
            rand = random.randint(cor - 100 if cor > 100 else 1, cor + 100 if cor < 901 else 1000)
        ret.append(rand)
    random.shuffle(ret)
    return ret

class Gui(tk.Tk):
    def __init__(self, easymode):
        tk.Tk.__init__(self)
        self.easymode = easymode
        self.geometry(f"800x600+{(self.winfo_screenwidth() // 2) - (800 // 2)}+{(self.winfo_screenheight() // 2) - (600 // 2) - 50}")
        self.resizable(False, False)
        self.title("Kinzoku")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._frame = None
        self.switch_frame(StartFrame)
    
    def switch_frame(self, frame_class):
        self._frame.destroy() if self._frame != None else None
        self._frame = frame_class(self, self.easymode)
        self._frame.pack()

    def on_close(self):
        print("Fenster wird geschlossen und Programm beendet.")
        self.destroy()
        sys.exit(0)

class StartFrame(tk.Frame):
    def __init__(self, window, easymode):
        tk.Frame.__init__(self, window, width=800, height=600)
        self.window = window
        self.pack_propagate(False)
        self.title = tk.Label(self, text="Willkommen bei Kinzoku", font=("Arial", 44))
        self.subtitle = tk.Label(self, text="Kinzoku ist ein Kopfrechentrainer.\nWenn du startest bekommst du 10 zufällig ausgewählte Rechnungen mit den vier Grundrechenarten im Bereich von 1 - 1000.", wraplength=750, font=("Arial", 24))
        self.easycheck = tk.Button(self, text="On" if easymode else "Off", font=("Arial", 10), width=4, height=1, command=self.toggle_easymode)
        self.easydesc = tk.Label(self, text="Easymode (Du bekommst 5 Antworten zur Auswahl)", font=("Arial", 14))
        self.start = tk.Button(self, text="Starten", command=self.start_run, font=("Arial", 22))
        self.title.pack(pady=50)
        self.subtitle.pack()
        self.easycheck.pack(pady=30, padx=(30, 5), side=tk.LEFT, anchor="s")
        self.easydesc.pack(pady=30, side=tk.LEFT, anchor="s")
        self.start.pack(pady=30, padx=30, side=tk.RIGHT, anchor="s")

    def toggle_easymode(self):
        self.window.easymode = not self.window.easymode
        self.easycheck["text"] = "On" if self.easycheck["text"] == "Off" else "Off"
    
    def start_run(self):
        print("started, easymode = " + str(self.window.easymode))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Kinzoku", description="Python Kopfrechentrainer")
    parser.add_argument("-g", "--gui", action="store_true", default=False, dest="use_gui", help="Öffnet das Programm mit einer grafischen Benutzeroberfläche")
    parser.add_argument("-e", "--easy", action="store_true", default=False, dest="use_easy", help="Aktiviert den Easy-Modus bei dem dir fünf potenziell richtige Ergebnisse vorgeschlagen werden")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, dest="use_verbose", help="Aktiviert den verbosen Modus")
    parser._actions[0].help = "Zeigt diese Hilfenachricht"
    args = parser.parse_args()
    easymode = args.use_easy
    verbose = args.use_verbose
    if not args.use_gui:
        print("GUI Version wird gestartet...")
        gui = Gui(easymode)
        gui.mainloop()
    clrscr()
    print("Willkommen bei Kinzoku!")
    print("Kinzoku ist ein Kopfrechentrainer.")
    print("Wenn du startest bekommst du 10 zufällig ausgewählte Rechnungen mit den vier Grundrechenarten im Bereich von 1 - 1000.\n")
    if easymode:
        print("Der Easy Mode ist aktiviert, dir werden bei jeder Rechnung 5 Vorschläge gegeben von denen einer richtig ist.")
    if input("Starten? (q für beenden): ")[:1].lower() == "q":
        sys.exit(0)
    count = 1
    correct = 0
    total = 0
    while True:
        clrscr()
        print(f"{count}. Rechnung:")
        calc = random.choice([gen_addition, gen_subtraction, gen_multiplication, gen_division])()
        if easymode:
            print(f"Vorschläge: {' | '.join(str(i) for i in gen_recomms(calc[2]))}")
        timer = time.time()
        res = input(f"{calc[0]} {calc[3]} {calc[1]}: ")
        while not res.isdigit():
            print("Bitte gib eine Zahl ein!")
            res = input(f"{calc[0]} {calc[3]} {calc[1]}: ")
        res = int(res)
        timer = round(time.time() - timer, 1)
        if res == calc[2]:
            print(f"Toll gemacht! Du hast die Rechnung in {int(timer) if timer == int(timer) else timer} Sekunde{'' if timer == 1.0 else 'n'} gelöst.")
            points = 3 if timer < 10 else (2 if timer < 20 else 1)
            total += points
            correct += 1
            print(f"Das gibt {points} Punkt{'' if points == 1 else 'e'} und somit hast du jetzt {total} Punkt{'' if total == 1 else 'e'}.")
        else:
            print(f"Wie schade! Du hast {int(timer) if timer == int(timer) else timer} Sekunde{'' if timer == 1.0 else 'n'} gebraucht und trotzdem falsch gerechnet.")
            print(f"Das richtige Ergebnis wäre {calc[2]} gewesen.")
        count += 1
        if count == 11 and str(input("Beenden?: ")) + "x" or input("Nächste Rechnung? (q für beenden): ")[:1].lower() == "q":
            clrscr()
            print(f"Du hast insgesamt {correct} / {count - 1} Rechnung{'en' if count - 1 != 1 else ''} gelöst und dabei {total} / {(count - 1) * 3} Punkten erreicht.")
            break
