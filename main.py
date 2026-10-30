# main.py - by Stav Shaham
# This file creates the graphical user interface.
# It communicates with tasks.py to manage the priority queue.

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tasks as ts

# Lower numbers represent higher priority.
PRIORITIES = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

# Converts priority numbers back into display text.
PRIORITY_NAMES = {
    1: "High",
    2: "Medium",
    3: "Low"
}

def add_task():
    """
    Read the task information from the GUI and add it
    to the priority queue.

    Time complexity:
        Adding to the heap takes O(log n).

        However, saving the tasks requires all tasks to be
        removed from a copied heap, which takes O(n log n).

        Overall complexity: O(n log n)
    """

    # Get the task name from the input field.
    task_name = root.task_entry.get().strip()
    # Get the selected priority from the dropdown menu.
    priority_name = root.priority_var.get()

    # Make sure the user entered a task name.
    if task_name:

        # Convert the priority name into a number.
        priority = PRIORITIES[priority_name]
        # Add the task to the priority queue.
        ts.add_task(
            task_name,
            priority
        )

        # Refresh the displayed task list.
        update_tasks()
        # Clear the input field.
        root.task_entry.delete(
            0,
            tk.END
        )

    else:
        # Show a warning if no task name was entered.
        messagebox.showwarning(
            "Warning",
            "You have to enter a task name"
        )


def on_toggle(task_object, variable, checkbox):
    """
    Update a task when its checkbox is clicked.

    Time complexity:
        Changing the task status takes O(1).

        Saving all tasks takes O(n log n).

        Overall complexity: O(n log n)
    """

    # Change the completed status of the task.
    ts.mark_done(
        task_object,
        variable.get()
    )

    # Update the checkbox's visual appearance.
    style_checkbox(
        checkbox,
        variable.get()
    )


def remove_task():
    """
    Remove all completed tasks.

    Time complexity:
        Checking all tasks takes O(n).

        Rebuilding the heap takes O(n).

        Saving the tasks takes O(n log n).

        Overall complexity: O(n log n)
    """

    # Remove completed tasks from the priority queue.
    ts.remove_completed_tasks()
    # Refresh the displayed tasks.
    update_tasks()


def move_up_priority(task):
    """
    Change a task's priority to one above it.
    
    Time complexity:
        Removing the item takes O(n).
        
        Appending takes O(1).
        
        Heapify takes O(n).
        
        Overall complexity: O(n)
    """

    # Return early if the task is already at the highest priority.
    if task["priority"] == 1:
        return
    
    # Move up the task's priority.
    ts.move_up_priority(task)

    # Refresh the displayed tasks.
    update_tasks()


def move_down_priority(task):
    """
    Change a task's priority to one below it.
    
    Time complexity:
        Removing the item takes O(n).
        
        Appending takes O(1).
        
        Heapify takes O(n).
        
        Overall complexity: O(n)
    """
    
    # Return early if the task is already at the lowest priority.
    if task["priority"] == 3:
        return
    
    # Move down the task's priority.
    ts.move_down_priority(task)

    # Refresh the displayed tasks.
    update_tasks()


def update_tasks():
    """
    Display all tasks in priority order.

    Time complexity:
        Removing the old widgets takes O(n).

        Getting all tasks in priority order takes O(n log n).

        Creating the new widgets takes O(n).

        Overall complexity: O(n log n)
    """

    # Get all existing widgets in the task frame.
    old_widgets = root.checkbox_frame.winfo_children()

    # Remove every old checkbox.
    for widget in old_widgets:
        widget.destroy()

    # Get the tasks in priority order.
    ordered_tasks = ts.view_tasks()

    # Create a checkbox for every task.
    for task in ordered_tasks:
        # Store the task's completed status.
        task_variable = tk.BooleanVar(
            value=task["done"]
        )

        # Convert the priority number into text.
        priority_text = PRIORITY_NAMES[
            task["priority"]
        ]

        # Display the priority before the task name.
        displayed_text = (
            "["
            + priority_text
            + "] "
            + task["name"]
        )

        # Create a frame for the widgets
        frame = tk.Frame(
            root.checkbox_frame
        )

        # Add the frame to the window.
        frame.pack(
            anchor='w'
        )

        # Create a move up button for the task.
        move_up_button = ttk.Button(
            frame,
            text="+P",
            width=2
        )
        
        # Add the move up button to the frame.
        move_up_button.pack(
            anchor="w",
            side="left"
        )

        # Connect this move up button to the on_toggle() function.
        # The default values in the lambda remember which task, variable, and checkbox belong together.
        move_up_button.config(
            command=lambda task_object=task:
            move_up_priority(
                task_object
            )
        )

        # Create a move down button for the task.
        move_down_button = ttk.Button(
            frame,
            text="-P",
            width=2
        )
                
        # Add the move down button to the frame.
        move_down_button.pack(
            anchor="w",
            side="left"
        )

        # Connect this move up button to the on_toggle() function.
        # The default values in the lambda remember which task, variable, and checkbox belong together.
        move_down_button.config(
            command=lambda task_object=task:
            move_down_priority(
                task_object
            )
        )

        # Create a checkbox for the task.
        checkbox = tk.Checkbutton(
            frame,
            text=displayed_text,
            variable=task_variable,
            bg="#1e1e1e",
            selectcolor="#1e1e1e",
            activebackground="#1e1e1e",
            anchor="w"
        )

        # Add the checkbox to the window.
        checkbox.pack(
            anchor="w",
            pady=3,
            side="left"
        )

        # Apply the correct style.
        style_checkbox(
            checkbox,
            task["done"]
        )

        # Connect this checkbox to the on_toggle() function.
        # The default values in the lambda remember which task, variable, and checkbox belong together.
        checkbox.config(
            command=lambda task_object=task,
            variable=task_variable,
            checkbox_object=checkbox:
            on_toggle(
                task_object,
                variable,
                checkbox_object
            )
        )

def style_checkbox(checkbox, done):
    """
    Change the appearance of a checkbox.

    Time complexity:
        O(1)

    Only one checkbox is modified.
    """

    if done:
        # Completed tasks appear gray and crossed out.
        checkbox.config(
            fg="gray",
            font=("Arial", 12, "overstrike")
        )

    else:
        # Incomplete tasks appear white.
        checkbox.config(
            fg="white",
            font=("Arial", 12, "normal")
        )


def on_frame_config(event):
    """
    Update the scrollable area when the frame changes.

    Time complexity:
        O(1)

    Only one canvas scroll region is updated.
    """

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def on_mousewheel(event):
    """
    Scroll the task list using the mouse wheel.

    Time complexity:
        O(1)

    Only one scrolling operation is performed.
    """

    # Ignore the event if there is no movement.
    if event.delta == 0:
        return

    # Scroll upward or downward.
    if event.delta > 0:
        canvas.yview_scroll(
            -1,
            "units"
        )
    else:
        canvas.yview_scroll(
            1,
            "units"
        )

# Create the main application window.
root = tk.Tk()

root.geometry("650x500")
root.title("Prioritized Todo List")

# Create the main frame.
root.main_frame = tk.Frame(
    root,
    padx=10,
    pady=10
)

root.main_frame.pack()

root.task_entry = tk.Entry(
    root.main_frame,
    width=30,

    # Dark background and white text.
    bg="#1e1e1e",
    fg="white",

    # Make the typing cursor visible.
    insertbackground="white",

    # Add a white border.
    highlightthickness=2,
    highlightbackground="white",
    highlightcolor="white",

    # Use a simple solid border.
    relief="solid",
    bd=1
)

root.task_entry.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

# Store the selected priority.
root.priority_var = tk.StringVar(
    value="Medium"
)

# Create the priority dropdown menu.
root.priority_menu = ttk.Combobox(
    root.main_frame,
    textvariable=root.priority_var,
    values=["High", "Medium", "Low"],
    state="readonly",
    width=10
)

root.priority_menu.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

# Create the Add Task button.
root.add_button = tk.Button(
    root.main_frame,
    text="Add Task",
    command=add_task
)

root.add_button.grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)

# Create a canvas for the scrollable task list.
canvas = tk.Canvas(
    root.main_frame,
    bg="#1e1e1e",
    highlightthickness=0
)

# Create the scrollbar.
scrollbar = ttk.Scrollbar(
    root.main_frame,
    orient="vertical",
    command=canvas.yview
)

# Create the frame that holds the checkboxes.
root.checkbox_frame = tk.Frame(
    canvas,
    bg="#1e1e1e"
)

# Place the checkbox frame inside the canvas.
canvas.create_window(
    (0, 0),
    window=root.checkbox_frame,
    anchor="nw"
)

# Update the scroll region when the checkbox frame changes.
root.checkbox_frame.bind(
    "<Configure>",
    on_frame_config
)

# Connect the scrollbar to the canvas.
canvas.configure(
    yscrollcommand=scrollbar.set
)

# Place the canvas in the window.
canvas.grid(
    row=1,
    column=0,
    columnspan=3,
    sticky="nsew"
)

# Place the scrollbar beside the canvas.
scrollbar.grid(
    row=1,
    column=3,
    sticky="ns"
)

# Enable mouse-wheel scrolling when the mouse enters the canvas.
canvas.bind(
    "<Enter>",
    lambda event: canvas.bind_all(
        "<MouseWheel>",
        on_mousewheel
    )
)

# Disable mouse-wheel scrolling when the mouse leaves the canvas.
canvas.bind(
    "<Leave>",
    lambda event: canvas.unbind_all(
        "<MouseWheel>"
    )
)

# Also enable scrolling when the mouse enters the checkbox frame.
root.checkbox_frame.bind(
    "<Enter>",
    lambda event: canvas.bind_all(
        "<MouseWheel>",
        on_mousewheel
    )
)

# Disable scrolling when the mouse leaves the checkbox frame.
root.checkbox_frame.bind(
    "<Leave>",
    lambda event: canvas.unbind_all(
        "<MouseWheel>"
    )
)

# Allow the canvas to expand when the window expands.
root.main_frame.grid_rowconfigure(
    1,
    weight=1
)

root.main_frame.grid_columnconfigure(
    0,
    weight=1
)

# Create the button for removing completed tasks.
root.remove_button = tk.Button(
    root.main_frame,
    text="Remove Done Tasks",
    command=remove_task
)

# Make the button span all three columns.
root.remove_button.grid(
    row=2,
    column=0,
    columnspan=3,
    padx=5,
    pady=5
)

# Load saved tasks when the application starts.
ts.load_data_from_file()
# Display the loaded tasks.
update_tasks()
# Start the application.
root.mainloop()