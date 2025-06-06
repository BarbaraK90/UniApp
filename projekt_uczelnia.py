import sqlite3
import tkinter as tk

from database_manager import DatabaseManager

from lecture_view import LectureView
from lecture_list import LectureList

conn = sqlite3.connect("data.db")
# Bez tego nie działają klucze obce
conn.execute("PRAGMA foreign_keys = ON")
database_manager = DatabaseManager(conn)
database_manager.create_tables()

lecture_view: LectureView | None = None

def handle_lecture_selected(lecture):
    global lecture_view
    if lecture_view is not None:
        lecture_view.forget()
        lecture_view.destroy()

    lecture_view = LectureView(right_panel, database_manager, lecture.id)
    lecture_view.pack(fill="both", expand=True)

def handle_lecture_deleted():
    global lecture_view
    if lecture_view is not None:
        lecture_view.forget()
        lecture_view.destroy()

window = tk.Tk()
window.title("Kolokwia")
window.geometry("1280x720")

left_panel = tk.Frame(window)
left_panel.place(relx=0, rely=0, relwidth=0.3, relheight=1.0)

right_panel = tk.Frame(window)
right_panel.place(relx=0.3, rely=0, relwidth=0.7, relheight=1.0)

lecture_list = LectureList(left_panel, database_manager, on_lecture_selected=handle_lecture_selected, on_lecture_deleted=handle_lecture_deleted)
lecture_list.pack(fill="both", expand=True)
lecture_list.reload_lectures()

window.mainloop()