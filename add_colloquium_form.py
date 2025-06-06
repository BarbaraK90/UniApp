import tkinter as tk
from colloquium import Colloquium

class AddColloquiumForm(tk.Frame):
    def __init__(self, master, lecture_id, on_adding = None):
        super().__init__(master)
        self.lecture_id = lecture_id
        self.on_adding = on_adding
        tk.Label(self, text="Dodaj kolokwium").pack()
        self.input = tk.Entry(self)
        self.input.pack()
        self.input.bind("<Return>", self.handle_input_return)
        self.add_button = tk.Button(self, text="Dodaj", command=self.handle_add_pressed)
        self.add_button.pack()

    def handle_input_return(self, _event):
        self.handle_add_pressed()

    def handle_add_pressed(self):
        if self.on_adding is None:
            return

        colloquium = Colloquium(name=self.input.get(), lecture_id=self.lecture_id)
        self.on_adding(colloquium)