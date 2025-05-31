import tkinter as tk
from colloquium import Colloquium

class AddColloquiumForm:
    def __init__(self, master, lecture_id, on_adding = None):
        self.lecture_id = lecture_id
        self.on_adding = on_adding
        self.frame = tk.Frame(master)
        tk.Label(self.frame, text="Dodaj kolokwium").pack()
        self.input = tk.Entry(self.frame)
        self.input.pack()
        self.add_button = tk.Button(self.frame, text="Dodaj", command=self.handle_add_pressed)
        self.add_button.pack()

    def pack(self):
        self.frame.pack(fill="x")

    def handle_add_pressed(self):
        if self.on_adding is None:
            return

        colloquium = Colloquium(name=self.input.get(), lecture_id=self.lecture_id)
        self.on_adding(colloquium)