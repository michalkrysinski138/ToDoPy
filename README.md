ToDoPy - Task List
ToDoPy is a task management application that allows users to create, edit, delete, and mark tasks as completed. The app uses a simple graphical user interface built with Tkinter and an SQLite database for storing data locally.

Files in the Project
The project consists of the following files:

app.py – The main application that runs the GUI and logic.
gui.py – The graphical user interface (GUI) built using Tkinter.
models.py – Logic for managing tasks, such as creating, deleting, and editing tasks.
db.py – Database operations with SQLite, such as connecting to the database, creating tables, and CRUD operations on tasks.
Installation
Install dependencies: Make sure you have Python installed (at least version 3.6). To install the required libraries, use the following command:


pip install -r requirements.txt
Create a virtual environment: You can use a virtual environment to manage project dependencies:


python -m venv .venv
source .venv/bin/activate  # For Unix systems
.venv\Scripts\activate  # For Windows
Run the application: After installing dependencies and activating the environment, run the application:


python app.py
How the Application Works?
The app allows you to:

Add tasks: You can add a task using the GUI.
View tasks: All tasks are displayed in a list with an option to filter them by completed or not.
Edit tasks: You can edit the task name.
Delete tasks: You can remove a task from the list.
Mark tasks as completed: You can mark a task as completed and change its status.
File Structure
app.py
This file is responsible for running the main application and user interface. It imports functions from gui.py, which are responsible for displaying the GUI, as well as functions from models.py and db.py that handle application logic and database operations.

gui.py
This file contains the user interface built with Tkinter. The GUI allows you to add tasks, display the task list, edit and delete tasks, as well as filter them by completed or not.

Functions:

run_gui() – Starts the main application loop.
display_tasks() – Responsible for displaying tasks in the GUI.
add_task_window() – Creates a window for adding new tasks.
edit_task() – Allows editing a task.
models.py
Contains the logic for task operations. Functions such as creating, editing, deleting tasks, and fetching tasks from the database.

Functions:

create_task() – Adds a new task to the database.
get_tasks() – Fetches all tasks from the database.
update_task() – Updates the status of a task (completed or not).
delete_task_from_db() – Deletes a task from the database.
db.py
Responsible for connecting to the SQLite database and managing the task table. It includes functions for connecting to the database, creating the table, and performing CRUD operations on tasks.

Functions:

connect_db() – Connects to the ToDoPy.db database.
create_table() – Creates the tasks table if it does not exist.
get_tasks() – Fetches all tasks from the database.
update_task() – Updates the status of a task.
delete_task() – Deletes a task.
