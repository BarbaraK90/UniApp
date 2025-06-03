import tkinter as tk
import re
from tkinter import ttk
from tkinter import messagebox

from database_manager import DatabaseManager
from lecture import Lecture
from student import Student
from colloquium import Colloquium
from colloquium_result import ColloquiumResult

from add_colloquium_form import AddColloquiumForm
from colloquium_list import ColloquiumList

class LectureView(tk.Frame):
    def __init__(self, master, database_manager: DatabaseManager, lecture_id: int):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.database_manager: DatabaseManager = database_manager
        self.lecture_id: int = lecture_id
        self.lecture: Lecture | None = None
        self.students: list[Student] | None = None
        self.colloquiums : list[Colloquium] | None = None
        self.edited_column = None
        self.edited_row = None
        self.edited_student_id = None
        self.edited_colloquium_id = None
        self.edit_entry: tk.Entry | None = None
        self.colloquium_results : dict[int, list[ColloquiumResult]] = {}
        self.tree: ttk.Treeview | None = None
        self.lecture_label: tk.Label = tk.Label(self)
        self.lecture_label.grid(row=0, column=0)
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=1, column=0)
        self.reload()
        self.add_colloquium_form = AddColloquiumForm(self, self.lecture_id, on_adding=self.handle_adding_colloquium)
        self.add_colloquium_form.grid(row=2, column=0)
        self.colloquium_list = ColloquiumList(self, self.database_manager, lecture_id, on_colloquium_deleted=self.handle_colloquium_deleted)
        self.colloquium_list.grid(row=3, column=0)

    def handle_colloquium_deleted(self, _colloquium):
        self.reload()

    def handle_adding_colloquium(self, colloquium):
        colloquium.insert(self.database_manager.conn)
        self.reload()
        self.colloquium_list.reload_colloquiums()

    def reload(self):
        self.load_data()
        self.lecture_label.config(text=self.get_label_text())
        if self.tree is not None:
            self.tree.forget()

        self.tree = self.get_tree()
        self.tree.bind("<Double-1>", self.handle_tree_double_click)
        self.tree.bind("<Configure>", self.handle_tree_resize)
        self.tree.pack()

    def handle_tree_resize(self, _event):
        if self.edit_entry is None:
            return

        self.place_edit_entry()

    def handle_tree_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        self.edited_column = self.tree.identify_column(event.x)
        self.edited_row = self.tree.identify_row(event.y)

        # Odczytanie id kolokwium z heading
        columns = self.tree['columns']
        column_id = int(self.edited_column.replace("#", "")) - 1 # index w Treeview jest od 1
        column_name = columns[column_id]
        # Tylko kolumny z wynikami kolokwium są edytowalne
        if not re.match("^c\\d+$", column_name):
            return

        self.edited_colloquium_id = int(column_name.replace("c", ""))
        self.edited_student_id = self.students[int(self.edited_row.replace("I", "")) - 1].id

        value = self.tree.set(self.edited_row, self.edited_column)

        self.edit_entry = tk.Entry(self.tree)
        self.place_edit_entry()
        self.edit_entry.insert(0, value)
        self.edit_entry.focus()
        self.edit_entry.bind("<Return>", self.handle_edit_entry_return)
        self.edit_entry.bind("<FocusOut>", self.handle_edit_entry_focus_out)

    def handle_edit_entry_return(self, _even):
        value = self.edit_entry.get()

        colloquium_result: ColloquiumResult | None = self.get_colloquium_result(self.edited_student_id, self.edited_colloquium_id)
        if value == "":
            self.tree.set(self.edited_row, self.edited_column, "")
            if colloquium_result is not None:
                colloquium_result.delete(self.database_manager.conn)
                self.colloquium_results[self.edited_student_id].remove(colloquium_result)
        else:
            try:
                points = float(value)
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowa wartość!")
                return
            self.tree.set(self.edited_row, self.edited_column, str(points))
            if colloquium_result is not None:
                colloquium_result.points = points
                colloquium_result.update(self.database_manager.conn)
            else:
                colloquium_result = ColloquiumResult(self.edited_colloquium_id, self.edited_student_id, points)
                colloquium_result.insert(self.database_manager.conn)
                self.colloquium_results[self.edited_student_id].append(colloquium_result)

        self.remove_edit_entry()

        avg = self.get_student_avg(self.edited_student_id)
        self.tree.set(self.edited_row, self.tree['columns'][-1], str(avg))

    def handle_edit_entry_focus_out(self, _event):
        self.remove_edit_entry()

    def place_edit_entry(self):
        x, y, width, height = self.tree.bbox(self.edited_row, self.edited_column)
        self.edit_entry.place(x=x, y=y, width=width, height=height)

    def remove_edit_entry(self):
        if self.edit_entry is None:
            return

        self.edit_entry.place_forget()
        self.edit_entry.destroy()
        self.edit_entry = None

    def load_data(self):
        self.lecture = self.database_manager.get_lecture(self.lecture_id)
        self.students = self.database_manager.get_students(self.lecture_id)
        self.colloquiums = self.database_manager.get_colloquiums(self.lecture_id)

    def get_label_text(self):
        return self.lecture.name

    def get_tree(self):
        columns = ["name", "number"]
        for colloquium in self.colloquiums:
            columns.append(f"c{colloquium.id}")

        columns.append("avg")

        tree = ttk.Treeview(self.tree_frame, columns=tuple(columns))
        # Usunięcie nieużywanej pierwszej kolumny na id
        tree['show'] = 'headings'
        tree.heading("name", text="Imię")
        tree.column("name", minwidth=0, width=100)
        tree.heading("number", text="Numer")
        tree.column("number", minwidth=0, width=100)
        tree.heading("avg", text="Średnia")
        tree.column("avg", minwidth=0, width=75)

        for colloquium in self.colloquiums:
            column_id = f"c{colloquium.id}"
            tree.heading(column_id, text=colloquium.name)
            tree.column(column_id, minwidth=0, width=75, stretch=False)

        for student in self.students:
            values = [student.name, student.album]
            colloquium_results = self.database_manager.get_colloquium_results(student.id)
            self.colloquium_results[student.id] = colloquium_results
            for colloquium in self.colloquiums:
                colloquium_result: ColloquiumResult | None = next(filter(lambda x: x.colloquium_id == colloquium.id, colloquium_results), None)
                if colloquium_result is not None:
                    values.append(colloquium_result.points)
                else:
                    values.append("")
            avg = self.get_student_avg(student.id)
            values.append(avg)
            tree.insert("", tk.END, values=tuple(values))

        return tree

    def get_student_avg(self, student_id):
        total_points = 0
        colloquium_results = self.colloquium_results[student_id]
        for colloquium_result in colloquium_results:
            total_points = total_points + colloquium_result.points
        return total_points / len(self.colloquiums)

    def get_colloquium_result(self, student_id, colloquium_id):
        # Pobieramy wynik kolokwium zapisany w self.colloquium_results
        colloquium_results = self.colloquium_results[student_id]
        return next(filter(lambda x: x.colloquium_id == colloquium_id, colloquium_results), None)
