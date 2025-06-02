class ColloquiumResult:
    def __init__(self,colloquium_id, student_id, points):
        self.colloquium_id = colloquium_id
        self.student_id = student_id
        self.points = points


    def insert(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO colloquium_results (
                colloquium_id,
                student_id,
                points
            ) VALUES (?, ?, ?)
        ''', (
            self.colloquium_id, self.student_id, self.points
        ))
        conn.commit()

    def update(self, conn):
        if self.colloquium_id is None or self.student_id is None:
            raise ValueError("ID kolokwium i studenta muszą być ustawione, aby wykonać update.")

        cursor = conn.cursor()
        cursor.execute('''
            UPDATE colloquium_results
            SET points = ?
            WHERE
                colloquium_id = ?
                AND student_id = ?
        ''', (
            self.points,
            self.colloquium_id,
            self.student_id
        ))
        conn.commit()

    def delete(self, conn):
        if self.colloquium_id is None or self.student_id is None:
            raise ValueError("ID kolokwium i studenta muszą być ustawione, aby wykonać delete.")

        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM colloquium_results WHERE colloquium_id = ? AND student_id = ?
        ''', (
            self.colloquium_id,
            self.student_id
        ))
        conn.commit()