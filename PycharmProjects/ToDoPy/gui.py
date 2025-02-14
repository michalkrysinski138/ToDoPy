import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from db import create_task, get_tasks, update_task
import sqlite3

def add_task():
    global task_entry
    task_name = task_entry.get()
    print("Wprowadzone zadanie:", task_name)
    if task_name:
        create_task(task_name)
        task_entry.delete(0, tk.END)
        display_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task name")


def edit_task(task_id):
    new_task_name = simpledialog.askstring("Edit Task", "Enter new task name:")

    if new_task_name:
        update_task_name_in_db(task_id, new_task_name)
        display_tasks()


def connect_db():
    print("Łączenie z bazą danych...")
    return sqlite3.connect('ToDoPy.db', timeout=10)


def update_task_name_in_db(task_id, new_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task_name = ? WHERE id = ?", (new_name, task_id))
    conn.commit()
    conn.close()


def mark_task_as_completed(task_id):

    update_task(task_id, 1)
    display_tasks()


def display_tasks():

    for widget in task_frame.winfo_children():
        widget.destroy()

    tasks = get_tasks()
    for task in tasks:
        task_id = task[0]
        task_name = task[1]
        completed = task[2]


        task_label = tk.Label(task_frame, text=task_name, width=50, fg="green" if completed else "black")
        task_label.pack()


        edit_button = tk.Button(task_frame, text="Edit", command=lambda t_id=task_id: edit_task(t_id))
        edit_button.pack()


        delete_button = tk.Button(task_frame, text="Delete", command=lambda t_id=task_id: delete_task(t_id))
        delete_button.pack()


        if completed == 0:
            complete_button = tk.Button(task_frame, text="Mark as Completed", command=lambda t_id=task_id: mark_task_as_completed(t_id))
            complete_button.pack()


def delete_task(task_id):

    delete_task_from_db(task_id)
    display_tasks()


def delete_task_from_db(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def run_gui():
    global task_entry, task_frame

    root = tk.Tk()
    root.title("ToDoPy - Task Manager")

    task_entry = tk.Entry(root, width=50)
    task_entry.pack(pady=10)

    add_button = tk.Button(root, text="Add Task", command=add_task)
    add_button.pack(pady=10)

    task_frame = tk.Frame(root)
    task_frame.pack(pady=20)

    display_tasks()

    root.mainloop()


if __name__ == "__main__":
    run_gui()