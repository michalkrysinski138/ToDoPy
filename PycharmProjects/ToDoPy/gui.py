import tkinter as tk
from tkinter import messagebox
from models import create_task, get_tasks, update_task, delete_task_from_db, get_task_name, update_task_name_in_db
import time

def update_time():
    current_time = time.strftime('%A, %Y-%m-%d %H:%M')
    time_label.config(text=current_time)
    time_label.after(60000, update_time)

def run_gui():
    global task_entry, task_frame, time_label, filter_var, search_entry

    root = tk.Tk()
    root.title("ToDoPy - Lista zadań")

    filter_var = tk.StringVar(value="all")

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    task_frame = tk.Frame(canvas)
    task_frame.configure(bg='#f0f0f0')

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=task_frame, anchor="nw")

    task_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    time_label = tk.Label(root, font=('Arial', 12), fg='black', anchor="w")
    time_label.pack(side="left", padx=10, pady=10, anchor="sw")

    update_time()
    display_tasks()

    add_button = tk.Button(root, text="Dodaj", command=add_task_window, bg='white', fg='#42a5f5', font=('Arial', 12, 'bold'))
    add_button.pack(pady=10, side="bottom", anchor="w")

    create_filter_buttons(root)


    search_label = tk.Label(root, text="Wyszukaj zadanie:", font=('Arial', 12))
    search_label.pack(side="top", anchor="w", padx=10, pady=5)

    search_entry = tk.Entry(root, font=('Arial', 12))
    search_entry.pack(side="top", anchor="w", padx=10, pady=5)

    search_button = tk.Button(root, text="Szukaj", command=search_tasks, bg='white', fg='#42a5f5', font=('Arial', 12, 'bold'))
    search_button.pack(side="top", anchor="w", padx=10, pady=10)

    root.mainloop()

def create_filter_buttons(root):
    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=10, anchor='w')

    all_button = tk.Radiobutton(filter_frame, text="Wszystkie", variable=filter_var, value="all", command=filter_tasks, font=('Arial', 12))
    all_button.pack(side="left", padx=5)

    completed_button = tk.Radiobutton(filter_frame, text="Ukończone", variable=filter_var, value="completed", command=filter_tasks, font=('Arial', 12))
    completed_button.pack(side="left", padx=5)

    not_completed_button = tk.Radiobutton(filter_frame, text="Nieukończone", variable=filter_var, value="not_completed", command=filter_tasks, font=('Arial', 12))
    not_completed_button.pack(side="left", padx=5)

def filter_tasks():
    selected_filter = filter_var.get()
    search_term = search_entry.get()

    if selected_filter == "all":
        tasks = get_tasks(search_term=search_term)
    elif selected_filter == "completed":
        tasks = get_tasks(completed=True, search_term=search_term)
    elif selected_filter == "not_completed":
        tasks = get_tasks(completed=False, search_term=search_term)

    display_tasks(tasks)

def search_tasks():
    search_term = search_entry.get()
    tasks = get_tasks(search_term=search_term)
    display_tasks(tasks)

def display_tasks(tasks=None):
    if tasks is None:
        tasks = get_tasks()

    for widget in task_frame.winfo_children():
        widget.destroy()

    for index, task in enumerate(tasks):
        task_id = task[0]
        task_name = task[1]
        completed = task[2]

        task_color = 'green' if completed else 'black'

        task_label = tk.Label(task_frame, text=f"{index + 1}. ", width=5, font=('Arial', 14, 'bold'), bg='#f0f0f0', anchor='w', fg=task_color)
        task_name_label = tk.Label(task_frame, text=task_name, width=50, font=('Arial', 14), bg='#f0f0f0', anchor='w', fg=task_color, wraplength=350)

        task_label.grid(row=index, column=0, padx=10, pady=5, sticky='w')
        task_name_label.grid(row=index, column=1, padx=10, pady=5, sticky='w')

        options_frame = tk.Frame(task_frame, bg='#f0f0f0')

        edit_button = tk.Button(options_frame, text="Edytuj", command=lambda t_id=task_id: edit_task(t_id), bg='#6A4C9C', fg='white', font=('Arial', 12, 'bold'))
        edit_button.grid(row=0, column=0, padx=5, pady=5)

        delete_button = tk.Button(options_frame, text="Usuń", command=lambda t_id=task_id: delete_task(t_id), bg='#6A4C9C', fg='white', font=('Arial', 12, 'bold'))
        delete_button.grid(row=0, column=1, padx=5, pady=5)

        if completed == 0:
            mark_button = tk.Button(options_frame, text="Gotowe", command=lambda t_id=task_id: mark_task_as_completed(t_id), bg='#6A4C9C', fg='white', font=('Arial', 12, 'bold'))
            mark_button.grid(row=0, column=2, padx=5, pady=5)
        else:
            unmark_button = tk.Button(options_frame, text="Anuluj", command=lambda t_id=task_id: unmark_task_as_completed(t_id), bg='#6A4C9C', fg='white', font=('Arial', 12, 'bold'))
            unmark_button.grid(row=0, column=2, padx=5, pady=5)

        options_frame.grid(row=index, column=2, padx=5, pady=5, sticky='w')

def edit_task(task_id):
    task_name = get_task_name(task_id)

    edit_window = tk.Toplevel()
    edit_window.title("Edytuj zadanie")

    label = tk.Label(edit_window, text="Edytuj zadanie", font=('Arial', 12))
    label.pack(pady=10)

    task_name_entry = tk.Entry(edit_window, width=50)
    task_name_entry.insert(0, task_name)
    task_name_entry.pack(pady=10)

    def update_task_name():
        new_name = task_name_entry.get()
        if new_name:
            update_task_name_in_db(task_id, new_name)
            edit_window.destroy()
            display_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task name")

    submit_button = tk.Button(edit_window, text="Edytuj", command=update_task_name, bg='white', fg='#42a5f5', font=('Arial', 12, 'bold'))
    submit_button.pack(pady=10)

def delete_task(task_id):
    delete_task_from_db(task_id)
    display_tasks()

def mark_task_as_completed(task_id):
    update_task(task_id, 1)
    display_tasks()

def unmark_task_as_completed(task_id):
    update_task(task_id, 0)
    display_tasks()

def add_task_window():
    add_window = tk.Toplevel()
    add_window.title("Dodaj zadanie")

    label = tk.Label(add_window, text="Dodaj zadanie:", font=('Arial', 12))
    label.pack(pady=10)

    task_name_entry = tk.Entry(add_window, width=50)
    task_name_entry.pack(pady=10)

    def add_task():
        task_name = task_name_entry.get()
        if task_name:
            create_task(task_name)
            add_window.destroy()
            display_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task name")

    submit_button = tk.Button(add_window, text="Dodaj zadanie", command=add_task, bg='white', fg='#42a5f5', font=('Arial', 12, 'bold'))
    submit_button.pack(pady=10)




