import argparse
import random
import os
import sys
import time
import ctypes
import tkinter as tk
from tkinter import ttk

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
    def __init__(self, easymode, endlessmode):
        tk.Tk.__init__(self)
        self.gamevars = {
            "easymode": easymode,
            "endlessmode": endlessmode,
            "round": 0,
            "correct": 0,
            "points": 0,
            "total": 0,
            "time": 0.0
        }
        self.calculation_list = []
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.critiqalfish.resilience")
        self.iconbitmap("resilience-icon.ico")
        self.call("source", "Azure-ttk-theme/azure.tcl")
        self.call("set_theme", "dark")
        self.geometry(f"800x600+{(self.winfo_screenwidth() // 2) - (800 // 2)}+{(self.winfo_screenheight() // 2) - (600 // 2) - 50}")
        self.resizable(False, False)
        self.title("Resilience")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._frame = None
        self.switch_frame(StartFrame)
    
    def switch_frame(self, frame_class):
        self.unbind("<Return>")
        self._frame.destroy() if self._frame != None else None
        self._frame = frame_class(self)
        self._frame.pack()

    def on_close(self):
        print("Fenster wird geschlossen und Programm beendet.")
        self.destroy()
        sys.exit(0)

class StartFrame(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self, window, width=800, height=600)
        self.window = window
        self.pack_propagate(False)

        self.title = ttk.Label(self, text="Willkommen bei Resilience", font=("Arial", 44))
        self.subtitle = ttk.Label(self, text="Resilience ist ein Kopfrechentrainer.\n\nWenn du startest bekommst du 10 zufällig ausgewählte Rechnungen mit den vier Grundrechenarten im Bereich von 1 - 1000.", justify="center", wraplength=750, font=("Arial", 24))
        self.optionsframe = ttk.Frame(self)
        self.themeswitch = ttk.Checkbutton(self.optionsframe, text="Dark Mode", command=self.change_theme, style="Switch.TCheckbutton")
        self.endlessswitch = ttk.Checkbutton(self.optionsframe, text="Endless Mode (Unendlich Rechnungen, anstatt 10)", command=self.toggle_endless, style="Switch.TCheckbutton")
        self.easyswitch = ttk.Checkbutton(self.optionsframe, text="Easymode (Du bekommst 5 Antworten zur Auswahl)", command=self.toggle_easymode, style="Switch.TCheckbutton")
        self.start = ttk.Button(self, text="Starten", command=lambda: window.switch_frame(CalcFrame), style="Accent.TButton")

        self.title.pack(pady=50)
        self.subtitle.pack()
        self.optionsframe.pack(padx=30, pady=30, side=tk.LEFT, anchor="s")
        self.themeswitch.pack(side=tk.TOP, anchor="w")
        self.endlessswitch.pack(side=tk.TOP, anchor="w")
        self.easyswitch.pack(side=tk.TOP, anchor="w")
        self.start.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.RIGHT, anchor="s")

        self.themeswitch.state(["selected"])
        self.endlessswitch.state(["selected"]) if window.gamevars["endlessmode"] else None
        self.easyswitch.state(["selected"]) if window.gamevars["easymode"] else None
        window.bind("<Return>", lambda _: window.switch_frame(CalcFrame))

    def change_theme(self):
        if self.window.call("ttk::style", "theme", "use") == "azure-dark":
            self.window.call("set_theme", "light")
            self.themeswitch["text"] = "Light Mode"
        else:
            self.window.call("set_theme", "dark")
            self.themeswitch["text"] = "Dark Mode"

    def toggle_endless(self):
        self.window.gamevars["endlessmode"] = not self.window.gamevars["endlessmode"]

    def toggle_easymode(self):
        self.window.gamevars["easymode"] = not self.window.gamevars["easymode"]    

class CalcFrame(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self, window, width=800, height=600)
        self.window = window
        self.pack_propagate(False)
        self.timer = 0.0
        self.points = 0
        self.calculation = random.choice([gen_addition, gen_subtraction, gen_multiplication, gen_division])()
        self.recomms = gen_recomms(self.calculation[2]) if window.gamevars["easymode"] else False

        self.topframe = ttk.Frame(self)
        self.title = ttk.Label(self.topframe, text=f"{window.gamevars['round'] + 1}. Rechnung:", font=("Arial", 22))
        self.timer_label = ttk.Label(self.topframe, text="0.0 Sekunden", font=("Arial", 22))
        self.middleframe = ttk.Frame(self)
        self.calculation_label = ttk.Label(self.middleframe, text=f"{self.calculation[0]} {self.calculation[3]} {self.calculation[1]}", font=("Arial", 30))
        if window.gamevars["easymode"]:
            self.recommframe = ttk.Frame(self.middleframe)
            self.recomm_buttons = []
            for i in range(5):
                self.recomm_buttons.append(ttk.Button(self.recommframe, text=f"{self.recomms[i]}", command=lambda i=i: self.on_finish(self.recomms[i]), style="Accent.TButton"))
        else:
            self.answer = ttk.Entry(self.middleframe, justify="center", validate="key", validatecommand=(self.register(self.input_validation), "%S", "%P"))
        self.result = ttk.Label(self.middleframe, text="", wraplength=700, font=("Arial", 20), justify="center")
        self.bottomframe = ttk.Frame(self)
        self.finish = ttk.Button(self.bottomframe, text="Fertig", command=self.on_finish)
        self.quit = ttk.Button(self.bottomframe, text="Frühzeitig\nBeenden" if not window.gamevars["endlessmode"] else "Beenden", command=self.on_quit)
        
        self.topframe.pack(side=tk.TOP, fill=tk.BOTH)
        self.title.pack(padx=10, pady=10, side=tk.LEFT, anchor="w")
        self.timer_label.pack(padx=10, pady=10, side=tk.RIGHT, anchor="e")
        self.middleframe.place(anchor="c", relx=.5, rely=.5)
        self.calculation_label.pack()
        if window.gamevars["easymode"]:
            self.recommframe.pack()
            for button in self.recomm_buttons:
                button.pack(side=tk.LEFT, padx=5, pady=5, ipady=5)
        else:
            self.answer.pack()
        self.result.pack()
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.quit.pack(padx=30, pady=30, ipadx=10, ipady=2 if not window.gamevars["endlessmode"] else 10, side=tk.LEFT, anchor="w")

        if window.gamevars["easymode"]:
            pass
        else:
            self.finish.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.RIGHT, anchor="e")
            self.answer.focus()
        self.tk_timer = self.after(100, self.update_timer)

    def input_validation(self, S, P):
        if P == "" and self.finish.instate(["!disabled"]):
            self.finish.state(["disabled"])
            self.window.unbind("<Return>")
            self.finish.configure(style="TButton")
        else:
            self.finish.state(["!disabled"])
            self.window.bind("<Return>", self.on_finish)
            self.finish.configure(style="Accent.TButton")
        if S.isdigit():
            return True
        else:
            self.bell()
            return False

    def on_finish(self, event = 0):
        if self.window.gamevars["easymode"]:
            self.recommframe.pack_forget()
        else:
            self.window.unbind("<Return>")
            self.answer.state(["disabled"])
        if not self.window.gamevars["easymode"] and not self.answer.get() == "" and int(self.answer.get()) == self.calculation[2] or event == self.calculation[2]:
            self.points = 3 if self.timer < 10.0 else 2 if self.timer < 20.0 else 1
            self.window.gamevars["correct"] += 1
            self.window.gamevars["points"] += self.points
            self.result["text"] = f"Toll gemacht! Du hast die Rechnung in {int(self.timer) if self.timer == int(self.timer) else self.timer} Sekunde{'' if self.timer == 1.0 else 'n'} gelöst.\n\nDas gibt {self.points} Punkt{'e' if self.points != 1 else ''}"
        else:
            self.result["text"] = f"Wie schade! Du hast {int(self.timer) if self.timer == int(self.timer) else self.timer} Sekunde{'' if self.timer == 1.0 else 'n'} gebraucht und trotzdem falsch gerechnet.\nDas richtige Ergebnis wäre {self.calculation[2]} gewesen."
        self.window.gamevars["round"] += 1
        self.window.gamevars["total"] += 3
        self.window.gamevars["time"] += round(self.timer, 1)
        self.window.calculation_list.append([self.window.gamevars["round"], f"{self.calculation[0]} {self.calculation[3]} {self.calculation[1]}", self.calculation[2], event, self.points, round(self.timer, 1)])
        self.timer_label["text"] = f"Gesamtpunkte: {self.window.gamevars['points']}"
        self.result.pack_configure(ipady=30)
        self.after_cancel(self.tk_timer)
        if self.window.gamevars["round"] < 10 or self.window.gamevars["endlessmode"]:
            self.finish.pack(padx=30, pady=30, ipadx=10, ipady=2, side=tk.RIGHT, anchor="e")
            self.finish.configure(text="Nächste\nRechnung", command=self.on_next, style="Accent.TButton")
        else:
            self.quit.pack_forget()
            self.finish.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.RIGHT, anchor="e")
            self.finish.configure(text="Beenden", command=self.on_next, style="Accent.TButton")
        self.window.bind("<Return>", self.on_next)

    def on_next(self, event = 0):
        self.window.switch_frame(CalcFrame if self.window.gamevars["round"] < 10 or self.window.gamevars["endlessmode"] else EndFrame)

    def on_quit(self):
        self.window.unbind("<Return>") if not self.window.gamevars["easymode"] else None
        self.after_cancel(self.tk_timer)
        self.window.switch_frame(EndFrame)

    def update_timer(self):
        self.timer = round(self.timer + 0.1, 1)
        self.timer_label["text"] = f"{self.timer} Sekunde{'n' if self.timer != 1.0 else '  '}"
        self.tk_timer = self.after(100, self.update_timer)

class EndFrame(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self, window, width=800, height=600)
        self.window = window
        self.pack_propagate(False)

        self.title = ttk.Label(self, text="Ergebnis:", font=("Arial", 44))
        self.calcs_stat = ttk.Label(self, text=f"Korrekt gelöst: {window.gamevars['correct']} / {window.gamevars['round']}", font=("Arial", 24))
        self.points_stat = ttk.Label(self, text=f"Punkte gesammelt: {window.gamevars['points']} / {window.gamevars['total']}", font=("Arial", 24))
        self.time_stat = ttk.Label(self, text=f"Gesamte Rechenzeit: {round(window.gamevars['time'], 1)} Sekunde{'n' if round(window.gamevars['time'], 1) != 1.0 else ''}", font=("Arial", 24))
        
        self.stats_tree = ttk.Treeview(self, columns=("no", "calculation", "result", "input", "points", "time"), height=6, show="headings")
        self.stats_tree.column("no", anchor="center", width=20)
        self.stats_tree.column("calculation", anchor="center", width=120)
        self.stats_tree.column("result", anchor="center", width=100)
        self.stats_tree.column("input", anchor="center", width=100)
        self.stats_tree.column("points", anchor="center", width=80)
        self.stats_tree.column("time", anchor="center", width=100)
        self.stats_tree.heading("no", text="#")
        self.stats_tree.heading("calculation", text="Rechnung")
        self.stats_tree.heading("result", text="Ergebnis")
        self.stats_tree.heading("input", text="Eingabe")
        self.stats_tree.heading("points", text="Punkte")
        self.stats_tree.heading("time", text="Zeit")

        self.again = ttk.Button(self, text="Erneut spielen", command=self.play_again)
        self.quit = ttk.Button(self, text="Beenden", command=window.on_close, style="Accent.TButton")

        self.title.pack(pady=40)
        self.calcs_stat.pack()
        self.points_stat.pack()
        self.time_stat.pack()
        self.stats_tree.pack(padx=50, pady=(20, 0))
        self.again.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.LEFT, anchor="s")
        self.quit.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.RIGHT, anchor="s")

        for v in window.calculation_list:
            self.stats_tree.insert(parent="", index=tk.END, values=(v[0], v[1], v[2], v[3], v[4], v[5]))

    def play_again(self):
        self.window.gamevars["round"], self.window.gamevars["correct"], self.window.gamevars["points"], self.window.gamevars["total"], self.window.gamevars["time"] = 0, 0, 0, 0, 0.0
        self.window.switch_frame(StartFrame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Resilience", description="Python Kopfrechentrainer")
    parser.add_argument("-g", "--gui", action="store_true", default=False, dest="use_gui", help="Öffnet das Programm mit einer grafischen Benutzeroberfläche")
    parser.add_argument("-e", "--easy", action="store_true", default=False, dest="use_easy", help="Aktiviert den Easy-Modus bei dem dir 5 potenziell richtige Ergebnisse vorgeschlagen werden")
    parser.add_argument("-i", "--infinity", action="store_true", default=False, dest="use_infinity", help="Aktiviert den Endless-Modus wobei dir unendlich anstatt 10 Rechnung gegeben werden")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, dest="use_verbose", help="Aktiviert den verbosen Modus")
    parser._actions[0].help = "Zeigt diese Hilfenachricht"
    args = parser.parse_args()
    easymode = args.use_easy
    endlessmode = args.use_infinity
    verbose = args.use_verbose
    if args.use_gui:
        print("GUI Version wird gestartet...")
        gui = Gui(easymode, endlessmode)
        gui.mainloop()
    clrscr()
    print("Willkommen bei Resilience!")
    print("Resilience ist ein Kopfrechentrainer.")
    print("Wenn du startest bekommst du 10 zufällig ausgewählte Rechnungen mit den vier Grundrechenarten im Bereich von 1 - 1000.\n")
    if easymode:
        print("Der Easy Mode ist aktiviert, dir werden bei jeder Rechnung 5 Vorschläge gegeben von denen einer richtig ist.")
    if endlessmode:
        print("Der Endless Mode ist aktiviert, dir werden unendlich anstatt 10 Rechnungen gegeben.")
    if easymode or endlessmode:
        print()
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
        if not endlessmode and count == 11 and str(input("Beenden?: ")) + "x" or input("Nächste Rechnung? (q für beenden): ")[:1].lower() == "q":
            clrscr()
            print(f"Du hast insgesamt {correct} / {count - 1} Rechnung{'en' if count - 1 != 1 else ''} gelöst und dabei {total} / {(count - 1) * 3} Punkten erreicht.")
            break
