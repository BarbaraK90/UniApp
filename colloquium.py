class Colloquium:
    def __init__(self,name,lecture_id, id = None):
        self.id = id
        self.name = name
        self.lecture_id = lecture_id

    def insert(self, conn):
        if self.id is not None:
            raise ValueError("ID kolokwium nie może być ustawione, aby wykonać insert.")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO colloquiums (
                name,
                lecture_id
            ) VALUES (?, ?)
        ''', (
            self.name, self.lecture_id
        ))
        conn.commit()
        self.id = cursor.lastrowid

    def update(self, conn):
        if self.id is None:
            raise ValueError("ID kolokwium musi być ustawione, aby wykonać update.")

        cursor = conn.cursor()
        cursor.execute('''
            UPDATE colloquiums
            SET name = ?,
                lecture_id = ?
            WHERE id = ?
        ''', (
            self.name,
            self.lecture_id,
            self.id
        ))
        conn.commit()

    def delete(self, conn):
        if self.id is None:
            raise ValueError("ID kolokwium musi być ustawione, aby wykonać delete.")

        cursor = conn.cursor()
        cursor.execute('''DELETE FROM colloquiums WHERE id = ?''',(self.id,))
        conn.commit()