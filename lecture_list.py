from database_manager import DatabaseManager
from lecture import Lecture
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class LectureList:
    def __init__(self, master, database_manager: DatabaseManager, on_lecture_selected, on_lecture_deleted):
        self.database_manager: DatabaseManager = database_manager
        self.on_lecture_selected = on_lecture_selected
        self.on_lecture_deleted = on_lecture_deleted
        self.lectures: list[Lecture] = []

        self.frame = tk.Frame(master)
        self.actions_frame = tk.Frame(self.frame)
        self.actions_frame.pack()
        self.import_button = tk.Button(self.actions_frame, text="Import...", command=self.handle_import_button_pressed)
        self.import_button.pack(pady=10, side="left")

        self.delete_button = tk.Button(self.actions_frame, text="Usuń", command=self.handle_delete_button_pressed)
        self.delete_button.pack(pady=10, side="left")

        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(pady=10, padx=20, fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.handle_lecture_selected)
        pass

    def pack(self):
        self.frame.pack(fill="both")

    def handle_import_button_pressed(self):
        file_name = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=(("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*"))
        )

        if file_name == '':
            return

        self.database_manager.import_csv(file_name)
        self.reload_lectures()

    def populate_lecture_list(self):
        self.listbox.delete(0, self.listbox.size())
        i = 0
        for lecture in self.lectures:
            i += 1
            self.listbox.insert(i, f"{lecture.department} - {lecture.name} ({lecture.term})")

    def reload_lectures(self):
        self.lectures = self.database_manager.get_lectures()
        self.populate_lecture_list()

    def handle_lecture_selected(self, _event):
        selection = self.listbox.curselection()

        if len(selection) == 0:
            return

        index = selection[0]
        lecture = self.lectures[index]

        if self.on_lecture_selected is None:
            return

        self.on_lecture_selected(lecture)

    def handle_delete_button_pressed(self):
        selection = self.listbox.curselection()

        if len(selection) == 0:
            return

        index = selection[0]
        lecture = self.lectures[index]
        lecture.delete(self.database_manager.conn)
        self.reload_lectures()

        if self.on_lecture_deleted is None:
            return

        self.on_lecture_deleted()