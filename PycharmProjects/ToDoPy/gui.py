import tkinter as tk
from tkinter import messagebox
from db import create_task, get_tasks, update_task

import tkinter as tk
from tkinter import messagebox
from db import create_task, get_tasks


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

def display_tasks():

    for widget in task_frame.winfo_children():
        widget.destroy()


    tasks = get_tasks()
    print("Pobrane zadania:", tasks)


    for task in tasks:
        task_label = tk.Label(task_frame, text=task[1], width=50)
        task_label.pack()

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