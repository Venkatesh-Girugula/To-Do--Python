import tkinter as tk
from tkinter import ttk, messagebox

def add_task():
    task = task_entry.get()
    #priority = priority_var.get()
    if task != "":
        # Format: Task | Priority | Status
        tasks.insert(tk.END, f"{task}        Not Done")
        task_entry.delete(0, tk.END)
        status_label.config(text="Task added successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def remove_task():
    try:
        selected = tasks.curselection()[0]
        tasks.delete(selected)
        status_label.config(text="Task removed successfully!")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def mark_task():
    try:
        selected = tasks.curselection()[0]
        task_text = tasks.get(selected)
        if "     Not Done" in task_text:
            new_text = task_text.replace("       Not Done", "        Done")
            tasks.delete(selected)
            tasks.insert(selected, new_text)
            status_label.config(text="Task marked as done!")
        else:
            new_text = task_text.replace("       Done", "        Not Done")
            tasks.delete(selected)
            tasks.insert(selected, new_text)
            status_label.config(text="Task marked as not done!")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task!")

def clear_all():
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?"):
        tasks.delete(0, tk.END)
        status_label.config(text="All tasks cleared!")

def search_task():
    query = search_entry.get().lower()
    if not query:
        return
    
    for i in range(tasks.size()):
        if query in tasks.get(i).lower():
            tasks.selection_clear(0, tk.END)
            tasks.selection_set(i)
            tasks.see(i)
            status_label.config(text=f"Found '{query}' in task {i+1}")
            return
    
    status_label.config(text=f"No task containing '{query}' found")

def on_key_press(event):
    if event.keysym == "Return" and event.state == 0:
        add_task()
    elif event.keysym == "Delete":
        remove_task()
    elif event.keysym == "space" and event.state == 4:  # Ctrl+Space
        mark_task()

# Set up the main window
root = tk.Tk()
root.title("Enhanced Todo List App")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# Create a custom style for buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("Add.TButton", background="#4CAF50", foreground="green")
style.configure("Remove.TButton", background="#f44336", foreground="blue")
style.configure("Mark.TButton", background="#2196F3", foreground="red")
style.configure("Clear.TButton", background="#FF9800", foreground="orange")

# Create frames for better organization
header_frame = tk.Frame(root, bg="#f0f0f0")
header_frame.pack(fill=tk.X, pady=10)

list_frame = tk.Frame(root, bg="#f0f0f0")
list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(fill=tk.X, padx=20, pady=10)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(fill=tk.X, padx=20, pady=10)

search_frame = tk.Frame(root, bg="#f0f0f0")
search_frame.pack(fill=tk.X, padx=20, pady=10)

status_frame = tk.Frame(root, bg="#f0f0f0")
status_frame.pack(fill=tk.X, padx=20, pady=10)

# Header
header_label = tk.Label(header_frame, text="Todo List Manager", font=("Arial", 16, "bold"), bg="#f0f0f0")
header_label.pack()

# Task list with scrollbar
task_frame = tk.Frame(list_frame)
task_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(task_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tasks = tk.Listbox(task_frame, width=70, height=12, selectbackground="#a0a0ff", 
                  font=("Arial", 10), yscrollcommand=scrollbar.set, bg="white")
tasks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=tasks)

# Task input section
task_label = tk.Label(input_frame, text="Task:", bg="#f0f0f0", font=("Arial", 10))
task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

task_entry = tk.Entry(input_frame, width=40, font=("Arial", 10))
task_entry.grid(row=0, column=1, padx=5, pady=5)
task_entry.bind("<KeyPress>", on_key_press)

#priority_label = tk.Label(input_frame, text="Priority:", bg="#f0f0f0", font=("Arial", 10))
#priority_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

#priority_var = tk.StringVar()
#priority_var.set("Medium")
#priority_dropdown = ttk.Combobox(input_frame, textvariable=priority_var, 
#                                values=["Low", "Medium", "High"], width=10)
#priority_dropdown.grid(row=0, column=3, padx=5, pady=5)

# Buttons section
add_button = ttk.Button(button_frame, text="Add Task ", command=add_task, style="Add.TButton")
add_button.grid(row=0, column=0, padx=5, pady=5)

remove_button = ttk.Button(button_frame, text="Remove Task ", command=remove_task, style="Remove.TButton")
remove_button.grid(row=0, column=1, padx=5, pady=5)

mark_button = ttk.Button(button_frame, text="Toggle Done", command=mark_task, style="Mark.TButton")
mark_button.grid(row=0, column=2, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="Clear All", command=clear_all, style="Clear.TButton")
clear_button.grid(row=0, column=3, padx=5, pady=5)

# Search section
search_label = tk.Label(search_frame, text="Search:", bg="#f0f0f0", font=("Arial", 10))
search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Search", command=search_task)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Status bar
status_label = tk.Label(status_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
status_label.pack(fill=tk.X)

# Start the main event loop
root.mainloop()
