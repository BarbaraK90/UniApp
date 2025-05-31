from student import Student
from lecture import Lecture
from colloquium import Colloquium
from colloquium_result import ColloquiumResult
import csv

class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        cursor = self.conn.cursor()

        self.create_lectures_table(cursor)
        self.create_students_table(cursor)
        self.create_colloquiums_table(cursor)
        self.create_colloquium_results_table(cursor)
        self.conn.commit()

    def create_lectures_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lectures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                department TEXT,
                field TEXT,
                speciality TEXT,
                lecture_type TEXT,
                degree TEXT,
                student_group TEXT,
                academic_year TEXT,
                year TEXT,
                term TEXT,
                term_number TEXT
            )
        ''')

    def create_students_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                album TEXT,
                tok_id TEXT,
                status TEXT,
                email TEXT,
                lecture_id INTEGER,
                FOREIGN KEY(lecture_id) REFERENCES lectures(id)
            )
        ''')

    def create_colloquiums_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS colloquiums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                lecture_id INTEGER,
                FOREIGN KEY(lecture_id) REFERENCES lectures(id)
            )
        ''')

    def create_colloquium_results_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS colloquium_results (
                colloquium_id INTEGER,
                student_id INTEGER,
                points FLOAT,
                PRIMARY KEY (student_id, colloquium_id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(colloquium_id) REFERENCES colloquiums(id)
            )
        ''')

    def import_csv(self, file_name):
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            lines = list(reader)

        lecture_data = {}
        i = 0

        while len(lines[i]) > 1:
            key = lines[i][0].strip().replace('"', '').replace(":", "")
            value = lines[i][1].strip().replace('"', '')
            lecture_data[key] = value
            i += 1

        # Tworzymy obiekt wykładu
        lecture = Lecture(
            name=lecture_data.get("Przedmiot", ""),
            department=lecture_data.get("Wydział", ""),
            field=lecture_data.get("Kierunek", ""),
            speciality=lecture_data.get("Specjalność", ""),
            lecture_type=lecture_data.get("System studiów", ""),
            degree=lecture_data.get("Rodzaj studiów", ""),
            group=lecture_data.get("Grupa studencka", ""),
            academic_year=lecture_data.get("Rok akademicki", ""),
            year=lecture_data.get("Rok studiów", ""),
            term=lecture_data.get("Semestr", ""),
            term_number=lecture_data.get("Numer semestru", "")
        )

        lecture.insert(self.conn)

        # Nagłówek studentów znajduje się na linii 11, dane studentów od linii 12
        for row in lines[i + 2:]:
            if len(row) < 6:
                continue  # Pomijamy niekompletne linie
            name = row[1].strip().replace('"', '')
            album = row[2].strip().replace('"', '').strip('/')
            tok_id = row[3].strip().replace('"', '')
            status = row[4].strip().replace('"', '')
            email = row[5].strip().replace('"', '')
            student = Student(name, album, tok_id, status, email, lecture.id)
            student.insert(self.conn)

    def __get_students(self, where = "1 = 1", param: tuple = ()):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, album, tok_id, status, email, lecture_id, id  FROM students WHERE " + where, param)
        rows = cursor.fetchall()

        students = [Student(*row) for row in rows]

        return students

    def get_students(self, lecture_id: int):
        return self.__get_students("lecture_id = ?", (lecture_id,))

    def get_student(self, student_id: int):
        return self.__get_students("id = ?", (student_id,))[0]

    def __get_lectures(self, where = "1 = 1", param: tuple = ()):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT name, department, field, speciality, lecture_type, degree, "group",
                   academic_year, year, term, term_number, id
            FROM lectures
            WHERE """ + where, param)
        rows = cursor.fetchall()

        lectures = [Lecture(*row) for row in rows]

        return lectures

    def get_lectures(self):
        return self.__get_lectures()

    def get_lecture(self, lecture_id: int):
        return self.__get_lectures("id = ?", (lecture_id,))[0]

    def __get_colloquiums(self, where = "1 = 1", param: tuple = ()):
        cursor = self.conn.cursor()

        cursor.execute("""
                    SELECT name, lecture_id, id
                    FROM colloquiums
                    WHERE """ + where, param)
        rows = cursor.fetchall()

        colloquiums = [Colloquium(*row) for row in rows]

        return colloquiums

    def get_colloquiums(self, lecture_id):
        return self.__get_colloquiums("lecture_id = ?", (lecture_id,))

    def get_colloquium(self, colloquium_id: int):
        return self.__get_colloquiums("id = ?", (colloquium_id,))[0]

    def __get_colloquium_results(self, where = "1 = 1", param: tuple = ()):
        cursor = self.conn.cursor()

        cursor.execute("""
                    SELECT colloquium_id, student_id, points
                    FROM colloquium_results
                    WHERE """ + where, param)
        rows = cursor.fetchall()

        colloquium_results = [ColloquiumResult(*row) for row in rows]

        return colloquium_results

    def get_colloquium_results(self, student_id: int):
        return self.__get_colloquium_results("student_id = ?", (student_id,))

    def get_colloquium_result(self, student_id: int, colloquium_id: int):
        return self.__get_colloquium_results("student_id = ? AND colloquium_id = ?", (student_id, colloquium_id))[0]