class Student:
    def __init__(self, name, album, tok_id, status, email, lecture_id, id = None):
        self.id = id
        self.name = name
        self.album = album
        self.tok_id = tok_id
        self.status = status
        self.email = email
        self.lecture_id = lecture_id

    def insert(self, conn):
        if self.id is not None:
            raise ValueError("ID studenta nie może być ustawione, aby wykonać insert.")

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (name, album, tok_id, status, email, lecture_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.name, self.album, self.tok_id, self.status, self.email, self.lecture_id))
        conn.commit()
        self.id = cursor.lastrowid

    def update(self, conn):
        if self.id is None:
            raise ValueError("ID studenta musi być ustawione, aby wykonać update.")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students
            SET name = ?, album = ?, tok_id = ?, status = ?, email = ?, lecture_id = ?
            WHERE id = ?
        """, (self.name, self.album, self.tok_id, self.status, self.email, self.lecture_id, self.id))
        conn.commit()