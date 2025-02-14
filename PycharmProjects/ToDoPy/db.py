import sqlite3


def connect_db():
    return sqlite3.connect('ToDoPy.db')


def create_task(task_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, completed) VALUES (?, ?)", (task_name, 0))
    conn.commit()
    conn.close()


def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(id, completed):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, id))
    conn.commit()
    conn.close()