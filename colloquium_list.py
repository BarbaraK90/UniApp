import tkinter as tk
from database_manager import DatabaseManager
from colloquium import Colloquium

class ColloquiumList(tk.Frame):
    def __init__(self, master, database_manager: DatabaseManager, lecture_id: int, on_colloquium_deleted = None):
        super().__init__(master)
        self.lecture_id = lecture_id
        self.database_manager: DatabaseManager = database_manager
        self.on_colloquium_deleted = on_colloquium_deleted
        self.colloquiums: list[Colloquium] | None = None
        self.listbox = tk.Listbox(self)
        self.listbox.pack()
        self.actions_frame = tk.Frame(self)
        self.actions_frame.pack()
        self.delete_button = tk.Button(self.actions_frame, text="Usuń", command=self.handle_delete_button_pressed)
        self.delete_button.pack(pady=10, side="left")
        self.reload_colloquiums()

    def reload_colloquiums(self):
        self.colloquiums = self.database_manager.get_colloquiums(self.lecture_id)
        self.populate_colloquium_list()

    def populate_colloquium_list(self):
        self.listbox.delete(0, self.listbox.size())
        i = 0
        for colloquium in self.colloquiums:
            i += 1
            self.listbox.insert(i, f"{colloquium.name}")

    def handle_delete_button_pressed(self):
        selection = self.listbox.curselection()

        if len(selection) == 0:
            return

        index = selection[0]
        colloquium = self.colloquiums[index]
        colloquium.delete(self.database_manager.conn)
        self.reload_colloquiums()

        if self.on_colloquium_deleted is None:
            return

        self.on_colloquium_deleted(colloquium)