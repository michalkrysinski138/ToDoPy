import sqlite3


def connect_db():
    print("Łączenie z bazą danych...")
    return sqlite3.connect('ToDoPy.db', timeout=10)


def create_task(task_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name, completed) VALUES (?, ?)", (task_name, 0))
        conn.commit()
        print(f"Task '{task_name}' has been added to the database.")
    except sqlite3.OperationalError as e:
        print("Błąd bazy danych:", e)
    finally:
        conn.close()


def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, completed FROM tasks")
    tasks = cursor.fetchall()
    print("Pobrane zadania z bazy:", tasks)
    conn.close()
    return tasks


def update_task(id, completed):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()