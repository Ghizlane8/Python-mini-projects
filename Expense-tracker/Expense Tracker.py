#!/usr/bin/env python3

import os

# -------------------------
# Data
# -------------------------

expenses = []


# -------------------------
# Core Functions
# -------------------------

def add_expense(expenses, category, amount, note, day):
    expenses.append({
        "category": category,
        "amount": amount,
        "note": note,
        "day": day
    })


def total_spent(expenses):
    return sum(exp["amount"] for exp in expenses)


def total_by_category(expenses):
    totals = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0) + exp["amount"]
    return totals


def max_expense(expenses):
    if not expenses:
        return None
    return max(expenses, key=lambda x: x["amount"])


def filter_by_category(expenses, category):
    return [e for e in expenses if e["category"] == category]


# -------------------------
# Saving & Loading
# -------------------------

def save_to_file(expenses, filename="expenses.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for exp in expenses:
            f.write(f"{exp['category']},{exp['amount']},{exp['note']},{exp['day']}\n")
    print("✔ Saved successfully.")


def load_from_file(filename="expenses.txt"):
    if not os.path.exists(filename):
        print("❌ File not found.")
        return []

    loaded = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            category, amount, note, day = line.strip().split(",")
            loaded.append({
                "category": category,
                "amount": float(amount),
                "note": note,
                "day": day
            })
    print("✔ Loaded successfully.")
    return loaded


# -------------------------
# Menu
# -------------------------

def menu():
    global expenses

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add new expense(s)")
        print("2. Show all expenses")
        print("3. Show totals per category")
        print("4. Show biggest expense")
        print("5. Save to file")
        print("6. Load from file")
        print("7. Exit")
        choice = input("Choose: ")

        # ADD EXPENSE
        if choice == "1":
            while True:
                category = input("Category (or 'done'): ")
                if category == "done":
                    break

                try:
                    amount = float(input("Amount: "))
                except:
                    print("Invalid amount. Retry.")
                    continue

                note = input("Note: ")
                day = input("Day (ex: 2025-03-01): ")

                add_expense(expenses, category, amount, note, day)
                print("✔ Expense added.")

        # SHOW ALL
        elif choice == "2":
            print("\n--- All Expenses ---")
            for exp in expenses:
                print(f"{exp['day']} - {exp['category']} - {exp['amount']}dh - {exp['note']}")

        # TOTALS BY CATEGORY
        elif choice == "3":
            print("\n--- Totals by Category ---")
            totals = total_by_category(expenses)
            for cat, value in totals.items():
                print(f"{cat:12} {value:.2f} dh")
            print(f"\nTOTAL SPENT: {total_spent(expenses):.2f} dh")

        # BIGGEST EXPENSE
        elif choice == "4":
            top = max_expense(expenses)
            if top:
                print("\n--- Biggest Expense ---")
                print(top)
            else:
                print("No expenses yet.")

        # SAVE
        elif choice == "5":
            save_to_file(expenses)

        # LOAD
        elif choice == "6":
            expenses = load_from_file()

        # EXIT
        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    menu()