from database_manager import DatabaseManager
from student import Student
from lecture import Lecture
from lecture_view import LectureView
from lecture_list import LectureList
import sqlite3
import tkinter as tk


conn = sqlite3.connect("data.db")
database_manager = DatabaseManager(conn)
database_manager.create_tables()

lecture_view: LectureView | None = None

def handle_lecture_selected(lecture):
    global lecture_view
    if lecture_view is not None:
        lecture_view.forget_and_destroy()

    lecture_view = LectureView(right_panel, database_manager, lecture.id)
    lecture_view.pack()

def handle_lecture_deleted():
    global lecture_view
    if lecture_view is not None:
        lecture_view.forget_and_destroy()

window = tk.Tk()
window.title("Kolokwia")
window.geometry("1280x720")

left_panel = tk.Frame(window, width=300)
left_panel.pack(side="left", fill="both", expand=True)

right_panel = tk.Frame(window, width=400)
right_panel.pack(side="left", fill="both", expand=True)

lecture_list = LectureList(left_panel, database_manager, on_lecture_selected=handle_lecture_selected, on_lecture_deleted=handle_lecture_deleted)
lecture_list.pack()
lecture_list.reload_lectures()

window.mainloop()