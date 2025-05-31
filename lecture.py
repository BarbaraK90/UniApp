class Lecture:
    def __init__(self, name, department, field, speciality, lecture_type, degree, group, academic_year, year, term, term_number, id = None):
        self.id = id
        self.name = name
        self.department = department
        self.field = field
        self.speciality = speciality
        self.lecture_type = lecture_type
        self.degree = degree
        self.group = group
        self.academic_year = academic_year
        self.year = year
        self.term = term
        self.term_number = term_number

    def insert(self, conn):
        if self.id is not None:
            raise ValueError("ID wykładu nie może być ustawione, aby wykonać insert.")

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO lectures (
                name,
                department,
                field,
                speciality,
                lecture_type,
                degree,
                student_group,
                academic_year,
                year,
                term,
                term_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.name, self.department, self.field, self.speciality,
            self.lecture_type, self.degree, self.group,
            self.academic_year, self.year, self.term, self.term_number
        ))
        conn.commit()
        self.id = cursor.lastrowid

    def update(self, conn):
        if self.id is None:
            raise ValueError("ID wykładu musi być ustawione, aby wykonać update.")

        cursor = conn.cursor()
        cursor.execute('''
            UPDATE lectures
            SET name = ?,
                department = ?,
                field = ?,
                speciality = ?,
                lecture_type = ?,
                degree = ?,
                group = ?,
                academic_year = ?,
                year = ?,
                term = ?,
                term_number = ?
            WHERE id = ?
        ''', (
            self.name,
            self.department,
            self.field,
            self.speciality,
            self.lecture_type,
            self.degree,
            self.group,
            self.academic_year,
            self.year,
            self.term,
            self.term_number,
            self.id
        ))
        conn.commit()

    def delete(self, conn):
        if self.id is None:
            raise ValueError("ID wykładu musi być ustawione, aby wykonać delete.")

        cursor = conn.cursor()
        cursor.execute('''DELETE FROM lectures WHERE id = ?''',(self.id,))
        conn.commit()