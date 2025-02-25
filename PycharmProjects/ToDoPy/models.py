import sqlite3


def connect_db():
    try:
        conn = sqlite3.connect('ToDoPy.db', timeout=10)
        return conn
    except sqlite3.Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None


def create_task(task_name):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name, completed) VALUES (?, ?)", (task_name, 0))
        conn.commit()
        conn.close()


def get_tasks(completed=None, search_term=None):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()


        query = "SELECT id, task_name, completed FROM tasks"
        conditions = []

        # Dodajemy warunek na 'completed' jeśli jest podany
        if completed is not None:
            conditions.append(f"completed = {completed}")


        if search_term:
            conditions.append(f"task_name LIKE '%{search_term}%'")


        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY completed DESC, id ASC"

        cursor.execute(query)
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    return []


def update_task(id, completed):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, id))
        conn.commit()
        conn.close()


def delete_task_from_db(task_id):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()


def get_task_name(task_id):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT task_name FROM tasks WHERE id = ?", (task_id,))
        task_name = cursor.fetchone()
        conn.close()
        if task_name:
            return task_name[0]
    return None


def update_task_name_in_db(task_id, new_name):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET task_name = ? WHERE id = ?", (new_name, task_id))
        conn.commit()
        conn.close()

