import json
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from csp import modelize_seaux


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    NORM_FONT = ("Helvetica", 10)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


class CreateConfigSeaux:

    def __init__(self):
        self.nb_seaux = 0
        self.contenance = []
        self.initial = []
        self.final = []
        self.max_etapes = 10
        self.conf_name = ""

    def start(self):
        def show_entry_fields():
            self.nb_seaux = int(e1.get())
            master.destroy()
            self.set_contenance()

        master = tk.Tk()
        master.title("Nb buckets")
        tk.Label(master, text="Number of buckets (max 6)").grid(row=0)
        e1 = tk.Entry(master)
        e1.grid(row=0, column=1)
        tk.Button(master, text='Ok', command=show_entry_fields).grid(row=1, column=1, sticky=tk.W)
        tk.mainloop()

    def set_contenance(self):
        master = tk.Tk()
        master.title("Contenance max")
        for i in range(self.nb_seaux):
            tk.Label(master, text=f"Size bucket {i + 1}").grid(row=i)
        entries = []

        for i in range(self.nb_seaux):
            entries.append(tk.Entry(master))
        for i, e in enumerate(entries):
            e.grid(row=i, column=1)

        def get_contenance():
            for i in range(self.nb_seaux):
                self.contenance.append(int(entries[i].get()))
            master.destroy()
            for i in range(self.nb_seaux):
                if self.contenance[i] <= 0:
                    msg = f'Bucket {i} cant containt any water'
                    popupmsg(msg)
                    raise Exception(msg)
            self.set_initial()

        tk.Button(master, text='Ok', command=get_contenance).grid(row=1 + self.nb_seaux, column=1, sticky=tk.W)
        tk.mainloop()

    def set_initial(self):
        master = tk.Tk()
        master.title("Inital state")
        for i in range(self.nb_seaux):
            tk.Label(master, text=f"Initial state of bucket {i + 1}").grid(row=i)
        entries = []

        for i in range(self.nb_seaux):
            entries.append(tk.Entry(master))
        for i, e in enumerate(entries):
            e.grid(row=i, column=1)

        def get_initial():
            for i in range(self.nb_seaux):
                self.initial.append(int(entries[i].get()))
            master.destroy()
            for i in range(self.nb_seaux):
                if self.contenance[i] < self.initial[i]:
                    msg = f'Bucket {i} containt more water at the begining than its own capacity'
                    popupmsg(msg)
                    raise Exception(msg)
            self.set_final()

        tk.Button(master, text='Ok', command=get_initial).grid(row=1 + self.nb_seaux, column=1, sticky=tk.W)
        tk.mainloop()

    def set_final(self):
        master = tk.Tk()
        master.title("Final state")
        for i in range(self.nb_seaux):
            tk.Label(master, text=f"Final state of bucket {i + 1}").grid(row=i)
        entries = []

        for i in range(self.nb_seaux):
            entries.append(tk.Entry(master))
        for i, e in enumerate(entries):
            e.grid(row=i, column=1)

        def get_final():
            for i in range(self.nb_seaux):
                self.final.append(int(entries[i].get()))
            master.destroy()
            for i in range(self.nb_seaux):
                if self.contenance[i] < self.final[i]:
                    msg = f'Bucket {i} containt more water at the end than its own capacity'
                    popupmsg(msg)
                    raise Exception(msg)
            if sum(self.initial) != sum(self.final):
                msg = f'You dont have the same quantity of water at the begining and at the end!'
                popupmsg(msg)
                raise Exception(msg)
            self.max_iter()

        tk.Button(master, text='Ok', command=get_final).grid(row=1 + self.nb_seaux, column=1, sticky=tk.W)
        tk.mainloop()

    def max_iter(self):
        def show_entry_fields():
            self.max_etapes = int(e1.get())
            master.destroy()
            self.end()

        master = tk.Tk()
        master.title("Nb max step")
        tk.Label(master, text="Number of step max").grid(row=0)
        e1 = tk.Entry(master)
        e1.grid(row=0, column=1)
        tk.Button(master, text='Ok', command=show_entry_fields).grid(row=1, column=1, sticky=tk.W)
        tk.mainloop()

    def config_name(self):
        def show_entry_fields():
            self.conf_name = str(e1.get())
            master.destroy()

        master = tk.Tk()
        master.title("Config Name")
        tk.Label(master, text="Name").grid(row=0)
        e1 = tk.Entry(master)
        e1.grid(row=0, column=1)
        tk.Button(master, text='Ok', command=show_entry_fields).grid(row=1, column=1, sticky=tk.W)
        tk.mainloop()

    def end(self):

        solution = modelize_seaux(nb_seaux=self.nb_seaux, max_etapes=self.max_etapes, contenance_max=self.contenance,
                                  contenu=self.initial, fin=self.final)
        if solution:
            self.config_name()
            config = {
                'nb seaux': self.nb_seaux,
                'nb etapes': solution['n_etape_fin'],
                'initial': self.initial,
                'final': self.final,
                'contenance max': self.contenance,
                'solution': solution['etat'][:solution['n_etape_fin']],
            }
            with open('configs/' + self.conf_name + '.json', 'w') as conf:
                json.dump(config, conf)
        else:
            popupmsg("This game have no solution")


def find_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Choose your file", initialdir=os.getcwd() + "/configs/",
                                           filetypes=[("json", ".json")])
    return file_path


if __name__ == '__main__':
    conf = CreateConfigSeaux()

    conf.start()
