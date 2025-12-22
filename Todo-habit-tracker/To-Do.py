# ------------------------------
# To-Do & Habit Tracker - Starter
# ------------------------------

def add_task(tasks, title, category):
    tasks.append({"title": title, "done": False, "category": category})


def mark_done(tasks, title):
    for task in tasks:
        if task["title"].lower() == title.lower():
            task["done"] = True
            return True
    return False


def tasks_by_category(tasks, category):
    return [t for t in tasks if t["category"].lower() == category.lower()]


def completion_stats(tasks):
    total = len(tasks)
    done = sum(t["done"] for t in tasks)
    percentage = (done / total * 100) if total else 0
    return total, done, percentage


def show_tasks(tasks, filter_status=None):
    print(f"{'Title':20} {'Category':10} {'Status'}")
    print("-" * 40)

    for t in tasks:
        status = "DONE" if t["done"] else "TODO"

        if filter_status == "done" and not t["done"]:
            continue
        if filter_status == "todo" and t["done"]:
            continue

        print(f"{t['title']:20} {t['category']:10} {status}")


def save_tasks(tasks, filename="tasks.txt"):
    with open(filename, "w") as f:
        for t in tasks:
            line = f"{t['title']},{t['category']},{t['done']}\n"
            f.write(line)


def load_tasks(filename="tasks.txt"):
    tasks = []
    try:
        with open(filename, "r") as f:
            for line in f:
                title, category, done = line.strip().split(",")
                tasks.append({
                    "title": title,
                    "category": category,
                    "done": done == "True"
                })
    except FileNotFoundError:
        print("⚠️ Fichier introuvable.")
    return tasks


# ------------------------------
# Menu principal
# ------------------------------

def main():
    tasks = []

    while True:
        print("\n--- TO-DO MENU ---")
        print("1. Add task")
        print("2. Mark task as done")
        print("3. Show all tasks")
        print("4. Show tasks by category")
        print("5. Show completion stats")
        print("6. Save tasks")
        print("7. Load tasks")
        print("8. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            title = input("Task title: ")
            category = input("Category: ")
            add_task(tasks, title, category)

        elif choice == "2":
            title = input("Title to mark as done: ")
            if mark_done(tasks, title):
                print("✔ Task marked as done.")
            else:
                print("❌ Task not found.")

        elif choice == "3":
            show_tasks(tasks)

        elif choice == "4":
            category = input("Category: ")
            filtered = tasks_by_category(tasks, category)
            show_tasks(filtered)

        elif choice == "5":
            total, done, perc = completion_stats(tasks)
            print(f"Total tasks: {total}")
            print(f"Completed : {done}")
            print(f"Progress  : {perc:.2f}%")

        elif choice == "6":
            save_tasks(tasks)
            print("💾 Tasks saved.")

        elif choice == "7":
            tasks = load_tasks()
            print("📂 Tasks loaded.")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice.")


# Run
main()
