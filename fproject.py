from datetime import datetime
from plyer import notification
import time
import threading

# List to store tasks
tasks = []
completed_tasks = []

# Function to send notification
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

# Function to add task
def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    deadline = input("Enter deadline (YYYY-MM-DD HH:MM): ")
    priority = input("Enter priority (High/Medium/Low): ")

    task = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "priority": priority,
        "status": "Pending"
    }

    tasks.append(task)
    print("Task added successfully!")

    # Calculate remaining time
    deadline_time = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    now = datetime.now()
    remaining = deadline_time - now

    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60

    message = f"{title} added!\nRemaining: {days}d {hours}h {minutes}m"
    print(message)

    send_notification("Task Added", message)

# Function to view tasks
def view_tasks():
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks):
        print(f"\nTask {i+1}")
        print("Title:", task["title"])
        print("Description:", task["description"])
        print("Deadline:", task["deadline"])
        print("Priority:", task["priority"])
        print("Status:", task["status"])

# Function to edit task
def edit_task():
    view_tasks()
    index = int(input("Enter task number to edit: ")) - 1

    if 0 <= index < len(tasks):
        tasks[index]["title"] = input("New title: ")
        tasks[index]["description"] = input("New description: ")
        tasks[index]["deadline"] = input("New deadline (YYYY-MM-DD HH:MM): ")
        tasks[index]["priority"] = input("New priority: ")

        print("Task updated successfully!")
        send_notification("Task Updated", tasks[index]["title"])
    else:
        print("Invalid task number")

# Function to delete task
def delete_task():
    view_tasks()
    index = int(input("Enter task number to delete: ")) - 1

    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        print("Task deleted successfully!")
        send_notification("Task Deleted", removed["title"])
    else:
        print("Invalid task number")

# Function to mark completed
def mark_completed():
    view_tasks()
    index = int(input("Enter task number completed: ")) - 1

    if 0 <= index < len(tasks):
        tasks[index]["status"] = "Completed"
        completed_tasks.append(tasks[index])
        send_notification("Completed", tasks[index]["title"])
    else:
        print("Invalid task number")

# Function to view completed tasks
def view_completed():
    if not completed_tasks:
        print("No completed tasks.")
        return

    for task in completed_tasks:
        print(task["title"], "-", task["status"])

# Background reminder checker
def check_reminders():
    notified = set()

    while True:
        now = datetime.now()

        for task in tasks:
            if task["status"] == "Completed":
                continue

            deadline_time = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
            remaining = (deadline_time - now).total_seconds()

            task_id = task["title"] + task["deadline"]

            if task_id in notified:
                continue

            # Overdue
            if remaining < 0:
                send_notification("Overdue Task", task["title"])
                notified.add(task_id)

            # Due now (0–60 sec)
            elif 0 <= remaining <= 60:
                send_notification("Due Now", task["title"])
                notified.add(task_id)

            # 10 minutes before
            elif 540 <= remaining <= 600:
                send_notification("Reminder", f"10 min left for {task['title']}")
                notified.add(task_id)

            # 1 hour before
            elif 3540 <= remaining <= 3600:
                send_notification("Reminder", f"1 hour left for {task['title']}")
                notified.add(task_id)

            # 1 day before
            elif 86340 <= remaining <= 86400:
                send_notification("Reminder", f"1 day left for {task['title']}")
                notified.add(task_id)

            # 5 days before
            elif 431940 <= remaining <= 432000:
                send_notification("Reminder", f"5 days left for {task['title']}")
                notified.add(task_id)

        time.sleep(20)

# Start background thread
threading.Thread(target=check_reminders, daemon=True).start()

# Main Program
while True:
    print("\n--- TASK MANAGER ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Mark Completed")
    print("6. View Completed Tasks")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        add_task()

    elif choice == '2':
        view_tasks()

    elif choice == '3':
        edit_task()

    elif choice == '4':
        delete_task()

    elif choice == '5':
        mark_completed()

    elif choice == '6':
        view_completed()

    elif choice == '7':
        print("Exiting...")
        break

    else:
        print("Invalid choice")