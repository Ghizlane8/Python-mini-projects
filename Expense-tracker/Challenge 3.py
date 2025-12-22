#!/usr/bin/env python3
"""
Expense Tracker Web App
- Flask + Tailwind modern UI
- Persistent storage in /mnt/data/expenses.txt
- Add expenses, view list, totals per category, biggest expense, filters
- Donut chart by category (Chart.js)
- Light / Dark mode toggle
"""

from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

DATA_FILE = "/mnt/data/expenses.txt"

# -------------------------
# Core logic
# -------------------------

def load_expenses():
    expenses = []
    if not os.path.exists(DATA_FILE):
        return expenses

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: category,amount,note,day
            parts = line.split(",")
            if len(parts) < 4:
                continue
            category = parts[0]
            try:
                amount = float(parts[1])
            except ValueError:
                continue
            # Join everything except first 2 and last as note (handles commas a bit)
            if len(parts) > 4:
                note = ",".join(parts[2:-1])
            else:
                note = parts[2]
            day = parts[-1]
            expenses.append({
                "category": category,
                "amount": amount,
                "note": note,
                "day": day
            })
    return expenses


def save_expenses(expenses):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for e in expenses:
            # Replace commas in note to avoid breaking CSV structure
            safe_note = (e["note"] or "").replace(",", ";")
            f.write(f"{e['category']},{e['amount']},{safe_note},{e['day']}\n")


def add_expense(expenses, category, amount, note, day):
    expenses.append({
        "category": category.strip(),
        "amount": amount,
        "note": note.strip(),
        "day": day.strip(),
    })


def total_spent(expenses):
    return sum(e["amount"] for e in expenses)


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        cat = e["category"] or "uncategorized"
        totals[cat] = totals.get(cat, 0) + e["amount"]
    return totals


def max_expense(expenses):
    if not expenses:
        return None
    return max(expenses, key=lambda e: e["amount"])


# -------------------------
# HTML Template (Tailwind + Chart.js + Dark mode)
# -------------------------

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Baali Ghizlane — Expense Tracker</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <script>
    // Tailwind config: enable class-based dark mode
    tailwind.config = {
      darkMode: 'class'
    };
  </script>

  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
  </style>

  <script>
    const THEME_KEY = "expense_tracker_theme";

    function applyTheme(theme) {
      const root = document.documentElement;
      if (theme === "dark") {
        root.classList.add("dark");
      } else {
        root.classList.remove("dark");
      }
    }

    function initTheme() {
      let saved = localStorage.getItem(THEME_KEY);
      if (saved !== "light" && saved !== "dark") {
        const prefersDark = window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches;
        saved = prefersDark ? "dark" : "light";
      }
      applyTheme(saved);
      return saved;
    }

    let currentTheme = initTheme();

    function updateThemeLabel() {
      const label = document.getElementById("theme-label");
      if (label) {
        label.textContent = currentTheme === "dark" ? "Dark" : "Light";
      }
    }

    function toggleTheme() {
      currentTheme = currentTheme === "dark" ? "light" : "dark";
      localStorage.setItem(THEME_KEY, currentTheme);
      applyTheme(currentTheme);
      updateThemeLabel();
    }

    document.addEventListener("DOMContentLoaded", updateThemeLabel);
  </script>
</head>
<body class="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-50">
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-blue-50 to-slate-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
    <div class="max-w-5xl mx-auto px-4 py-8">

      <!-- HEADER -->
      <header class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div class="inline-flex items-center gap-2 rounded-full border border-sky-300/60 bg-sky-50 px-3 py-1 text-xs uppercase tracking-[0.2em] text-sky-600 dark:bg-slate-900 dark:border-slate-700 dark:text-sky-300">
            <span class="h-2 w-2 rounded-full bg-sky-400 shadow-[0_0_10px_rgba(56,189,248,0.7)]"></span>
            Expense Tracker
          </div>
          <h1 class="mt-3 text-2xl sm:text-3xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">
            Daily Expense Tracker <span class="text-sky-600 dark:text-sky-400">&amp; Analytics</span>
          </h1>
          <p class="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Track your daily expenses, see totals by category, and keep everything saved in a file.
          </p>
        </div>

        <!-- THEME TOGGLE -->
        <div class="flex items-center justify-end">
          <button type="button" onclick="toggleTheme()"
                  class="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-3 py-1 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800">
            <span class="h-2 w-2 rounded-full bg-slate-900 dark:bg-yellow-300"></span>
            <span id="theme-label">Light</span>
          </button>
        </div>
      </header>

      <!-- STATS CARDS -->
      <section class="grid gap-4 mb-6 sm:grid-cols-3">
        <div class="rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
          <div class="flex items-center justify-between">
            <span class="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Total spent</span>
          </div>
          <div class="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-50">
            {{ "%.2f"|format(total_spent) }} <span class="text-base text-slate-500 dark:text-slate-400">DH</span>
          </div>
          <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">All categories combined</p>
        </div>

        <div class="rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
          <div class="flex items-center justify-between">
            <span class="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Number of expenses</span>
          </div>
          <div class="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-50">
            {{ expenses|length }}
          </div>
          <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Rows currently displayed</p>
        </div>

        <div class="rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
          <div class="flex items-center justify-between">
            <span class="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Average expense</span>
          </div>
          <div class="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-50">
            {{ "%.2f"|format(avg_expense) }} <span class="text-base text-slate-500 dark:text-slate-400">DH</span>
          </div>
          <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Based on filtered expenses</p>
        </div>
      </section>

      <div class="grid gap-6 lg:grid-cols-[minmax(0,1.4fr),minmax(0,1fr)]">

        <!-- LEFT COLUMN: FORM + TABLE -->
        <div class="space-y-6">

          <!-- ADD EXPENSE FORM -->
          <section class="rounded-2xl border border-slate-200 bg-white px-4 py-4 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
            <div class="flex items-center justify-between gap-2 mb-2">
              <h2 class="text-sm font-semibold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <span class="inline-flex h-6 w-6 items-center justify-center rounded-full bg-sky-50 text-xs text-sky-600 border border-sky-200 dark:bg-slate-800 dark:border-slate-600 dark:text-sky-300">+</span>
                Add an expense
              </h2>
            </div>

            <form method="post" action="{{ url_for('add') }}" class="grid gap-3 sm:grid-cols-2">
              <div class="sm:col-span-1">
                <label class="block text-xs text-slate-600 dark:text-slate-300 mb-1">Category</label>
                <input name="category" required
                       class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 dark:bg-slate-950 dark:border-slate-700 dark:text-slate-50 dark:placeholder:text-slate-500"
                       placeholder="food, transport, shopping..." />
              </div>

              <div class="sm:col-span-1">
                <label class="block text-xs text-slate-600 dark:text-slate-300 mb-1">Amount (DH)</label>
                <input name="amount" required type="number" step="0.01" min="0"
                       class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 dark:bg-slate-950 dark:border-slate-700 dark:text-slate-50 dark:placeholder:text-slate-500"
                       placeholder="e.g. 45.50" />
              </div>

              <div class="sm:col-span-1">
                <label class="block text-xs text-slate-600 dark:text-slate-300 mb-1">Day / Date</label>
                <input name="day"
                       class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 dark:bg-slate-950 dark:border-slate-700 dark:text-slate-50 dark:placeholder:text-slate-500"
                       placeholder="2025-03-01 or Monday" />
              </div>

              <div class="sm:col-span-1">
                <label class="block text-xs text-slate-600 dark:text-slate-300 mb-1">Note (optional)</label>
                <input name="note"
                       class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 dark:bg-slate-950 dark:border-slate-700 dark:text-slate-50 dark:placeholder:text-slate-500"
                       placeholder="e.g. lunch, taxi, groceries..." />
              </div>

              <div class="sm:col-span-2 flex items-center justify-between pt-1">
                <p class="text-[11px] text-slate-500 dark:text-slate-400">
                  Tip: avoid using <span class="font-mono">,</span> in the note (they are replaced internally).
                </p>
                <button
                  class="inline-flex items-center gap-1 rounded-xl bg-sky-500 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-sky-200 hover:bg-sky-600 transition">
                  Save expense
                </button>
              </div>
            </form>
          </section>

          <!-- FILTERS -->
          <section class="rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
            <form method="get" action="{{ url_for('index') }}" class="grid gap-3 sm:grid-cols-3 items-end">
              <div>
                <label class="block text-xs text-slate-600 dark:text-slate-300 mb-1">Filter by category</label>
                <select name="category"
                        class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 dark:bg-slate-950 dark:border-slate-700 dark:text-slate-50">
                  <option value="">All</option>
                  {% for cat in all_categories %}
                    <option value="{{ cat }}" {% if cat == category_filter %}selected{% endif %}>{{ cat }}</option>
                  {% endfor %}
                </select>
              </div>

              <div>
                <label class="block text-xs text-slate-600 dark:text-slate-300 mb-1">Filter by day / date</label>
                <input name="day" value="{{ day_filter }}"
                       class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 dark:bg-slate-950 dark:border-slate-700 dark:text-slate-50 dark:placeholder:text-slate-500"
                       placeholder="e.g. Monday or 2025-03-01" />
              </div>

              <div class="flex gap-2">
                <button class="flex-1 rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-xs font-medium text-slate-800 hover:bg-slate-100 transition dark:bg-slate-800 dark:border-slate-600 dark:text-slate-100 dark:hover:bg-slate-700">
                  Apply filters
                </button>
                <a href="{{ url_for('index') }}"
                   class="rounded-xl border border-slate-300 bg-white px-3 py-2 text-[11px] text-slate-700 hover:bg-slate-50 transition dark:bg-slate-900 dark:border-slate-700 dark:text-slate-100 dark:hover:bg-slate-800">
                  Reset
                </a>
              </div>
            </form>
          </section>

          <!-- EXPENSES TABLE -->
          <section class="rounded-2xl border border-slate-200 bg-white px-4 py-4 overflow-x-auto shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
            <div class="flex items-center justify-between mb-2">
              <h2 class="text-sm font-semibold text-slate-900 dark:text-slate-50">Expenses ({{ expenses|length }})</h2>
            </div>

            {% if expenses %}
              <table class="w-full text-xs text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-[11px] uppercase text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    <th class="py-2 pr-3">Day / Date</th>
                    <th class="py-2 pr-3">Category</th>
                    <th class="py-2 pr-3 text-right">Amount</th>
                    <th class="py-2 pr-3">Note</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                  {% for e in expenses %}
                    <tr class="hover:bg-slate-50 dark:hover:bg-slate-800">
                      <td class="py-2 pr-3 align-top text-slate-700 dark:text-slate-300">{{ e.day }}</td>
                      <td class="py-2 pr-3 align-top">
                        <span class="inline-flex rounded-full bg-sky-50 px-2 py-0.5 text-[11px] text-sky-700 border border-sky-100 dark:bg-slate-800 dark:border-slate-600 dark:text-sky-300">
                          {{ e.category or "—" }}
                        </span>
                      </td>
                      <td class="py-2 pr-3 align-top text-right font-mono text-slate-900 dark:text-slate-50">
                        {{ "%.2f"|format(e.amount) }}
                      </td>
                      <td class="py-2 pr-3 align-top text-slate-600 dark:text-slate-300">
                        {{ e.note or "—" }}
                      </td>
                    </tr>
                  {% endfor %}
                </tbody>
              </table>
            {% else %}
              <p class="text-xs text-slate-500 dark:text-slate-400">No expenses to show with these filters.</p>
            {% endif %}
          </section>

        </div>

        <!-- RIGHT COLUMN: CHART + CATEGORY TOTALS + BIGGEST -->
        <div class="space-y-4">

          <!-- DONUT CHART -->
          <section class="rounded-2xl border border-slate-200 bg-white px-4 py-4 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
            <h2 class="text-sm font-semibold text-slate-900 dark:text-slate-50 mb-2">Spending breakdown</h2>
            {% if category_labels %}
              <div class="h-52">
                <canvas id="categoryChart"></canvas>
              </div>
              <p class="mt-2 text-[11px] text-slate-500 dark:text-slate-400">
                Based on filtered expenses by category.
              </p>
            {% else %}
              <p class="text-xs text-slate-500 dark:text-slate-400">
                Add some expenses to see the chart.
              </p>
            {% endif %}
          </section>

          <!-- TOTALS PER CATEGORY -->
          <section class="rounded-2xl border border-slate-200 bg-white px-4 py-4 shadow-sm shadow-slate-200 dark:bg-slate-900 dark:border-slate-700 dark:shadow-slate-900">
            <h2 class="text-sm font-semibold text-slate-900 dark:text-slate-50 mb-2">Totals by category</h2>

            {% if totals_by_category %}
              <ul class="space-y-2 text-xs">
                {% for cat, value in totals_by_category.items() %}
                  <li class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <span class="h-2 w-2 rounded-full bg-sky-400/80"></span>
                      <span class="text-slate-800 dark:text-slate-100">{{ cat }}</span>
                    </div>
                    <span class="font-mono text-slate-900 dark:text-slate-50">{{ "%.2f"|format(value) }} DH</span>
                  </li>
                {% endfor %}
              </ul>
            {% else %}
              <p class="text-xs text-slate-500 dark:text-slate-400">No categories yet.</p>
            {% endif %}
          </section>

          <!-- BIGGEST EXPENSE -->
          <section class="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-4 shadow-sm shadow-amber-100 dark:bg-amber-900/20 dark:border-amber-600/60 dark:shadow-slate-900">
            <h2 class="text-sm font-semibold text-amber-900 dark:text-amber-200 mb-2">Biggest expense</h2>

            {% if biggest %}
              <div class="space-y-1 text-xs text-amber-900 dark:text-amber-100">
                <div class="flex items-center justify-between">
                  <span class="text-[11px] uppercase tracking-wide text-amber-600 dark:text-amber-300">Amount</span>
                  <span class="font-mono text-sm">{{ "%.2f"|format(biggest.amount) }} DH</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-[11px] uppercase tracking-wide text-amber-600 dark:text-amber-300">Category</span>
                  <span class="rounded-full bg-amber-100 border border-amber-200 px-2 py-0.5 text-[11px] dark:bg-amber-900/40 dark:border-amber-500">
                    {{ biggest.category }}
                  </span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-[11px] uppercase tracking-wide text-amber-600 dark:text-amber-300">Day</span>
                  <span>{{ biggest.day }}</span>
                </div>
                <div class="mt-2">
                  <span class="text-[11px] uppercase tracking-wide text-amber-600 dark:text-amber-300">Note</span>
                  <p class="mt-1 text-[11px] bg-amber-100 border border-amber-200 rounded-xl px-2 py-1 dark:bg-amber-900/40 dark:border-amber-500">
                    {{ biggest.note or "—" }}
                  </p>
                </div>
              </div>
            {% else %}
              <p class="text-xs text-amber-800/90 dark:text-amber-200/80">Add some expenses to see the biggest one here.</p>
            {% endif %}
          </section>

        </div>
      </div>

      <footer class="mt-8 text-[11px] text-slate-500 dark:text-slate-400 text-center">
        Baali Ghizlane — Expense Tracker
      </footer>
    </div>
  </div>

  <!-- Chart.js Donut Script -->
  <script>
    const categoryLabels = {{ category_labels | tojson }};
    const categoryValues = {{ category_values | tojson }};

    document.addEventListener("DOMContentLoaded", function () {
      const ctx = document.getElementById("categoryChart");
      if (!ctx || !categoryLabels.length) return;

      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: categoryLabels,
          datasets: [{
            data: categoryValues,
            borderWidth: 1,
            backgroundColor: [
              "#38bdf8",
              "#a855f7",
              "#f97316",
              "#22c55e",
              "#eab308",
              "#ec4899",
              "#0ea5e9",
              "#6366f1",
            ],
          }]
        },
        options: {
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                usePointStyle: true,
              }
            }
          },
          cutout: "60%",
          responsive: true,
          maintainAspectRatio: false,
        }
      });
    });
  </script>
</body>
</html>
"""

# -------------------------
# Routes
# -------------------------

@app.route("/", methods=["GET"])
def index():
    expenses = load_expenses()

    # Filters: filter by category and day
    category_filter = request.args.get("category", "").strip()
    day_filter = request.args.get("day", "").strip()

    filtered = []
    for e in expenses:
        if category_filter and e["category"] != category_filter:
            continue
        if day_filter and e["day"] != day_filter:
            continue
        filtered.append(e)

    totals = total_by_category(filtered)
    total = total_spent(filtered)
    biggest = max_expense(filtered)
    avg = total / len(filtered) if filtered else 0.0

    all_categories = sorted({e["category"] for e in expenses if e["category"]})

    # For the donut chart
    category_labels = list(totals.keys())
    category_values = list(totals.values())

    return render_template_string(
        HTML_TEMPLATE,
        expenses=filtered,
        total_spent=total,
        totals_by_category=totals,
        biggest=biggest,
        avg_expense=avg,
        category_filter=category_filter,
        day_filter=day_filter,
        all_categories=all_categories,
        category_labels=category_labels,
        category_values=category_values,
    )


@app.route("/add", methods=["POST"])
def add():
    expenses = load_expenses()

    category = request.form.get("category", "").strip()
    amount_raw = request.form.get("amount", "0").strip()
    note = request.form.get("note", "").strip()
    day = request.form.get("day", "").strip() or "unknown"

    try:
        amount = float(amount_raw)
    except ValueError:
        amount = 0.0

    if category and amount > 0:
        add_expense(expenses, category, amount, note, day)
        save_expenses(expenses)

    return redirect(url_for("index"))


if __name__ == "__main__":
    # Debug for development, disable in production
    app.run(host="0.0.0.0", port=8000, debug=True)
