import sqlite3

def connect_db():
    try:
        print("Łączenie z bazą danych...")
        conn = sqlite3.connect('ToDoPy.db', timeout=10)
        return conn
    except sqlite3.Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None

def create_table():
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

def create_task(task_name):
    try:
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task_name, completed) VALUES (?, ?)", (task_name, 0))
            conn.commit()
            print(f"Task '{task_name}' has been added to the database.")
        else:
            print("Nie udało się połączyć z bazą danych.")
    except sqlite3.OperationalError as e:
        print("Błąd bazy danych:", e)
    finally:
        if conn:
            conn.close()

def get_tasks():
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_name, completed FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        print("Pobrane zadania z bazy:", tasks)
        return tasks
    return []

def update_task(id, completed):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, id))
        conn.commit()
        conn.close()

def delete_task(task_id):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()