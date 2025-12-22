# ----------------------------
# Student Management System
# Challenge 1
# ----------------------------

# ---------- Functions ----------

def add_student(students, name, age, grade):
    student = {"name": name, "age": age, "grade": grade}
    students.append(student)

def average_grade(students):
    if not students:
        return 0
    return sum(s["grade"] for s in students) / len(students)

def best_student(students):
    if not students:
        return None
    return max(students, key=lambda s: s["grade"])

def failing_students(students, threshold):
    return [s for s in students if s["grade"] < threshold]

def group_by_age(students):
    groups = {}
    for s in students:
        age = s["age"]
        groups[age] = groups.get(age, 0) + 1
    return groups

# ---------- File Handling ----------

def save_to_file(students, filename="students.txt"):
    with open(filename, "w") as f:
        for s in students:
            f.write(f"{s['name']},{s['age']},{s['grade']}\n")

def load_from_file(filename="students.txt"):
    students = []
    try:
        with open(filename, "r") as f:
            for line in f:
                name, age, grade = line.strip().split(",")
                students.append({
                    "name": name,
                    "age": int(age),
                    "grade": float(grade)
                })
    except FileNotFoundError:
        print("⚠️ File not found.")
    return students

# ---------- Menu Loop ----------

def main():
    students = []

    while True:
        print("\n===== STUDENT MENU =====")
        print("1. Add students")
        print("2. Show summary")
        print("3. Show best student")
        print("4. Show failing students")
        print("5. Save to file")
        print("6. Load from file")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            while True:
                name = input("Enter name (or 'done' to stop): ")
                if name.lower() == "done":
                    break

                try:
                    age = int(input("Age: "))
                    grade = float(input("Grade: "))
                except ValueError:
                    print("❌ Invalid number!")
                    continue

                add_student(students, name, age, grade)
                print("✔️ Student added!")

        elif choice == "2":
            print("\n--- Summary ---")
            print("Name        Age   Grade")
            print("------------------------")
            for s in students:
                print(f"{s['name']:<12}{s['age']:<6}{s['grade']:.2f}")

        elif choice == "3":
            s = best_student(students)
            if s:
                print(f"\nBest student: {s['name']} ({s['grade']})")
            else:
                print("No students.")

        elif choice == "4":
            threshold = float(input("Fail threshold: "))
            fails = failing_students(students, threshold)
            print("\nFailing students:")
            for s in fails:
                print(f"- {s['name']} ({s['grade']})")

        elif choice == "5":
            save_to_file(students)
            print("💾 Saved!")

        elif choice == "6":
            students = load_from_file()
            print("📂 Loaded!")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid option.")

main()
