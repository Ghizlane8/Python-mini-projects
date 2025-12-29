# 🐍 Python Mini Projects – Fundamentals Practice Pack

## 📖 Overview
This repository is a curated collection of **Python mini-projects** designed to strengthen core programming fundamentals through **hands-on, practical applications**.

Each project simulates a **real-world use case** and focuses on writing clean, structured, and maintainable Python code.  
The goal is to consolidate essential concepts that serve as a foundation for **Data Science, Software Engineering, and AI projects**.

---

## 🚀 What You’ll Find in This Repository
Through these projects, you will practice:

- Python fundamentals (syntax, control flow, functions)
- Data structures (lists, dictionaries)
- File handling (read/write, persistence)
- Input validation and error handling
- Problem decomposition and modular design
- Console-based application logic (CLI)

All projects are implemented using **pure Python (standard library only)**.

---
[PyChallenges.html](https://github.com/user-attachments/files/24370609/PyChallenges.html)<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Python Challenge Pack – Choose Your Mission</title>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg: #020617;
      --bg-gradient-1: rgba(56, 189, 248, 0.16);
      --bg-gradient-2: rgba(168, 85, 247, 0.16);
      --panel: #020617;
      --accent: #38bdf8;
      --accent-strong: #0ea5e9;
      --accent-soft: rgba(56, 189, 248, 0.15);
      --accent-2: #a855f7;
      --text-main: #e5e7eb;
      --text-muted: #9ca3af;
      --border-subtle: rgba(148, 163, 184, 0.32);
      --shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.9);
      --radius-xl: 18px;
      --radius-pill: 999px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top left, var(--bg-gradient-1), transparent 55%),
        radial-gradient(circle at bottom right, var(--bg-gradient-2), transparent 55%),
        var(--bg);
      color: var(--text-main);
      line-height: 1.6;
      padding: 40px 16px 48px;
    }

    main {
      max-width: 1100px;
      margin: 0 auto;
    }

    header {
      text-align: center;
      margin-bottom: 24px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 4px 14px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-subtle);
      background: rgba(15, 23, 42, 0.95);
      color: var(--text-muted);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 14px;
    }

    .badge-dot {
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--accent);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.9);
    }

    h1 {
      font-size: clamp(2.1rem, 3.4vw, 2.7rem);
      margin-bottom: 8px;
      letter-spacing: -0.03em;
    }

    .subtitle {
      color: var(--text-muted);
      max-width: 700px;
      margin: 0 auto;
      font-size: 0.95rem;
    }

    .highlight-note {
      margin: 18px auto 6px;
      max-width: 720px;
      padding: 12px 16px;
      border-radius: var(--radius-xl);
      border: 1px solid rgba(56, 189, 248, 0.7);
      background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.22), rgba(15, 23, 42, 0.96));
      box-shadow: 0 0 26px rgba(56, 189, 248, 0.35);
      font-size: 0.92rem;
      color: var(--accent-strong);
    }

    .highlight-note strong {
      font-weight: 700;
    }

    .grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      gap: 18px;
      margin-top: 26px;
    }

    @media (min-width: 880px) {
      .grid {
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      }
    }

    .challenge-card {
      position: relative;
      background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.12), rgba(15, 23, 42, 0.98));
      border-radius: var(--radius-xl);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-soft);
      padding: 18px 18px 16px;
      overflow: hidden;
      isolation: isolate;
    }

    .challenge-card::before {
      content: "";
      position: absolute;
      inset: -40%;
      background:
        radial-gradient(circle at top right, rgba(168, 85, 247, 0.18), transparent 55%);
      opacity: 0;
      transition: opacity 0.35s ease;
      pointer-events: none;
      z-index: -1;
    }

    .challenge-card:hover::before {
      opacity: 1;
    }

    .challenge-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 8px;
    }

    .challenge-tag {
      font-size: 0.68rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.14em;
      margin-bottom: 2px;
    }

    .challenge-title {
      font-size: 1.04rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pill {
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 3px 10px;
      border-radius: var(--radius-pill);
      border: 1px solid rgba(148, 163, 184, 0.65);
      color: var(--text-muted);
      white-space: nowrap;
    }

    .challenge-body {
      font-size: 0.9rem;
      margin-top: 6px;
    }

    .challenge-body p {
      margin-bottom: 8px;
      color: var(--text-main);
    }

    .accent-chip {
      display: inline-block;
      font-size: 0.7rem;
      padding: 2px 9px;
      border-radius: var(--radius-pill);
      background: var(--accent-soft);
      color: var(--accent-strong);
      margin-bottom: 6px;
    }

    .challenge-body ul,
    .challenge-body ol {
      margin-left: 18px;
      margin-bottom: 6px;
    }

    .challenge-body li {
      margin-bottom: 4px;
    }

    .sub-title {
      font-weight: 600;
      margin-top: 4px;
      margin-bottom: 2px;
      color: var(--accent-2);
      font-size: 0.9rem;
    }

    .muted {
      color: var(--text-muted);
      font-size: 0.86rem;
    }

    code,
    pre {
      font-family: "Fira Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 0.84rem;
      background: rgba(15, 23, 42, 0.98);
      border-radius: 10px;
      border: 1px solid rgba(51, 65, 85, 0.85);
      color: #e5e7eb;
    }

    code.inline {
      padding: 2px 5px;
      border-radius: 6px;
      background: rgba(15, 23, 42, 0.96);
    }

    pre {
      padding: 8px 10px;
      overflow-x: auto;
      margin: 8px 0;
    }

    hr.divider {
      border: 0;
      border-top: 1px dashed rgba(148, 163, 184, 0.5);
      margin: 28px 0 14px;
    }

    footer {
      text-align: center;
      font-size: 0.82rem;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div class="badge">
        <span class="badge-dot"></span>
        Python Challenge Pack
      </div>

      <h1>Python Mini-Projects – Choose Your Challenge</h1>
      <p class="subtitle">
        Each challenge combines lists, dictionaries, loops, functions, conditionals, files, and string formatting.
      </p>

      <div class="highlight-note">
        <strong>Instruction:</strong> choose <strong>one</strong> challenge from the list below and implement it in a Python notebook.
        
      </div>
    </header>

    <section class="grid">

      <!-- CHALLENGE 1 -->
      <article class="challenge-card">
        <div class="challenge-header">
          <div>
            <div class="challenge-tag">Challenge 1</div>
            <h2 class="challenge-title">Student Management &amp; Grade Analytics System</h2>
          </div>
          <div class="pill">Lists · Dicts · Files</div>
        </div>
        <div class="challenge-body">
          <p><span class="accent-chip">Goal:</span> Build a small student management system that lets you input students, save them, reload them, and analyze their grades.</p>

          <p class="sub-title">Data model</p>
          <p>Use a <strong>list of dictionaries</strong> like:</p>
          <pre><code>students = [
    {"name": "Lina", "age": 18, "grade": 16.5},
    {"name": "Omar", "age": 20, "grade": 14.0},
]</code></pre>

          <p class="sub-title">1. Input &amp; validation</p>
          <ul>
            <li>Ask the user repeatedly to enter:
              <ul>
                <li>name (string)</li>
                <li>age (integer)</li>
                <li>grade (float)</li>
              </ul>
            </li>
            <li>Stop when the user types <code class="inline">"done"</code> for the name.</li>
            <li>Use <code class="inline">try/except</code> to handle invalid ages/grades (non-numeric input).</li>
          </ul>

          <p class="sub-title">2. Core functions</p>
          <p>Implement at least these functions:</p>
          <pre><code>def add_student(students, name, age, grade): ...
def average_grade(students): ...
def best_student(students): ...
def failing_students(students, threshold): ...
def group_by_age(students): ...</code></pre>
          <ul>
            <li><code class="inline">best_student</code> returns the dict of the student with the highest grade.</li>
            <li><code class="inline">failing_students</code> returns a list of students whose grade is below a given threshold.</li>
            <li><code class="inline">group_by_age</code> returns a dict like <code class="inline">{18: 3, 19: 5, 20: 2}</code>.</li>
          </ul>

          <p class="sub-title">3. Sorting &amp; summaries</p>
          <ul>
            <li>Print students sorted:
              <ul>
                <li>by grade (descending)</li>
                <li>by name (alphabetically)</li>
              </ul>
            </li>
            <li>Print a summary table using f-strings with alignment:</li>
          </ul>
          <pre><code>Name        Age   Grade
-----------------------
Lina        18    16.50
Omar        20    14.00</code></pre>

          <p class="sub-title">4. File handling</p>
          <ul>
            <li>Save all students to a text file (e.g. <code class="inline">"students.txt"</code>) in a CSV-like format:</li>
          </ul>
          <pre><code>Lina,18,16.5
Omar,20,14.0</code></pre>
          <ul>
            <li>Load the file back, rebuild the <code class="inline">students</code> list, and re-run the analysis.</li>
          </ul>

          <p class="sub-title">5. Menu system</p>
          <p>Create a looped menu:</p>
          <pre><code>1. Add students
2. Show summary
3. Show best student
4. Show failing students
5. Save to file
6. Load from file
7. Exit</code></pre>
          <p>Use <code class="inline">if / elif / else</code> to handle choices and show an error for invalid options.</p>
        </div>
      </article>

      <!-- CHALLENGE 2 -->
      <article class="challenge-card">
        <div class="challenge-header">
          <div>
            <div class="challenge-tag">Challenge 2</div>
            <h2 class="challenge-title">Text Analysis &amp; Word Frequency Explorer</h2>
          </div>
          <div class="pill">Strings · Dicts · Files</div>
        </div>
        <div class="challenge-body">
          <p><span class="accent-chip">Goal:</span> Create a text-analysis tool that can analyze a paragraph or small text file.</p>

          <p class="sub-title">1. Input options</p>
          <ul>
            <li>Ask the user whether to:
              <ul>
                <li>enter text manually, or</li>
                <li>load text from a file (e.g. <code class="inline">"text.txt"</code>).</li>
              </ul>
            </li>
            <li>If loading from file, use <code class="inline">try/except</code> to handle missing file errors.</li>
          </ul>

          <p class="sub-title">2. Cleaning &amp; splitting</p>
          <p>Write a function:</p>
          <pre><code>def clean_text(text):
    # lowercase, remove punctuation, replace multiple spaces with one</code></pre>
          <p>Then split the cleaned text into words using <code class="inline">.split()</code>.</p>

          <p class="sub-title">3. Frequency dictionary</p>
          <ul>
            <li>Build a dict like <code class="inline">{"word": count}</code>.</li>
            <li>Compute:
              <ul>
                <li>total number of words</li>
                <li>number of unique words</li>
              </ul>
            </li>
          </ul>

          <p class="sub-title">4. Top words &amp; sorting</p>
          <ul>
            <li>Convert the dict to a list of <code class="inline">(word, count)</code> tuples.</li>
            <li>Sort:
              <ul>
                <li>by frequency descending,</li>
                <li>alphabetically when counts are equal.</li>
              </ul>
            </li>
            <li>Print the top <strong>10</strong> words in a neat table:</li>
          </ul>
          <pre><code>Word           Count
--------------------
python         12
code           9</code></pre>

          <p class="sub-title">5. Extra statistics</p>
          <ul>
            <li>Find the <strong>longest word</strong> and <strong>shortest word</strong>.</li>
            <li>Count how many words start with a <strong>vowel</strong>.</li>
            <li>Count how many words have length <strong>&ge; 7</strong>.</li>
          </ul>

          <p class="sub-title">6. Report file</p>
          <ul>
            <li>Write a report file <code class="inline">"report.txt"</code> containing:
              <ul>
                <li>total words,</li>
                <li>unique words,</li>
                <li>top 10 words with counts,</li>
                <li>longest and shortest word.</li>
              </ul>
            </li>
          </ul>
        </div>
      </article>

      <!-- CHALLENGE 3 -->
      <article class="challenge-card">
        <div class="challenge-header">
          <div>
            <div class="challenge-tag">Challenge 3</div>
            <h2 class="challenge-title">Expense Tracker with Persistent Storage</h2>
          </div>
          <div class="pill">Dicts · Loops · Files</div>
        </div>
        <div class="challenge-body">
          <p><span class="accent-chip">Goal:</span> Build a console-based expense tracker that keeps track of daily expenses.</p>

          <p class="sub-title">Data model</p>
          <p>Use a list of dictionaries:</p>
          <pre><code>expenses = [
    {"category": "food", "amount": 45.0, "note": "lunch", "day": "2025-03-01"},
]</code></pre>

          <p class="sub-title">1. Adding expenses</p>
          <ul>
            <li>In a loop, ask for:
              <ul>
                <li>category (string)</li>
                <li>amount (float)</li>
                <li>note (string, optional)</li>
                <li>date or day (string like <code class="inline">"2025-03-01"</code> or <code class="inline">"Monday"</code>)</li>
              </ul>
            </li>
            <li>Use <code class="inline">try/except</code> to handle invalid amounts.</li>
            <li>Stop when the user types <code class="inline">"done"</code> for category.</li>
          </ul>

          <p class="sub-title">2. Core functions</p>
          <pre><code>def add_expense(expenses, category, amount, note, day): ...
def total_spent(expenses): ...
def total_by_category(expenses): ...
def max_expense(expenses): ...
def filter_by_category(expenses, category): ...</code></pre>
          <ul>
            <li><code class="inline">total_by_category</code> returns a dict like <code class="inline">{"food": 120.5, "transport": 30}</code>.</li>
            <li><code class="inline">max_expense</code> returns the single expense dict with the largest amount.</li>
          </ul>

          <p class="sub-title">3. Summaries</p>
          <ul>
            <li>Show:
              <ul>
                <li>total spent,</li>
                <li>a table of totals per category.</li>
              </ul>
            </li>
          </ul>
          <pre><code>Category      Total
-------------------
food          120.50
transport      30.00</code></pre>

          <p class="sub-title">4. Saving &amp; loading</p>
          <ul>
            <li>Save all expenses to <code class="inline">"expenses.txt"</code> in a structured format.</li>
            <li>Load them back into the program to verify persistence.</li>
          </ul>

          <p class="sub-title">5. Menu system</p>
          <p>Add options such as:</p>
          <pre><code>1. Add new expense(s)
2. Show all expenses
3. Show totals per category
4. Show biggest expense
5. Save to file
6. Load from file
7. Exit</code></pre>
          <p>Handle invalid choices with a message and do not crash.</p>

          <p class="sub-title">6. Bonus</p>
          <ul>
            <li>Filter expenses by category and day (e.g. all <code class="inline">"food"</code> on <code class="inline">"Monday"</code>).</li>
            <li>Show average expense amount.</li>
          </ul>
        </div>
      </article>

      <!-- CHALLENGE 4 -->
      <article class="challenge-card">
        <div class="challenge-header">
          <div>
            <div class="challenge-tag">Challenge 4</div>
            <h2 class="challenge-title">To-Do &amp; Habit Tracker</h2>
          </div>
          <div class="pill">Dicts · Logic · Files</div>
        </div>
        <div class="challenge-body">
          <p><span class="accent-chip">Goal:</span> Create a to-do / habit tracking system that uses lists, dicts, file I/O, and some logic.</p>

          <p class="sub-title">Data model</p>
          <p>Use a list of dictionaries:</p>
          <pre><code>tasks = [
    {"title": "Study Python", "done": False, "category": "study"},
]</code></pre>

          <p class="sub-title">1. Adding tasks</p>
          <ul>
            <li>Ask the user to enter:
              <ul>
                <li>task title</li>
                <li>category (e.g. <code class="inline">"study"</code>, <code class="inline">"work"</code>, <code class="inline">"personal"</code>)</li>
              </ul>
            </li>
            <li>Set <code class="inline">done</code> to <code class="inline">False</code> initially.</li>
          </ul>

          <p class="sub-title">2. Core functions</p>
          <pre><code>def add_task(tasks, title, category): ...
def mark_done(tasks, title): ...
def tasks_by_category(tasks, category): ...
def completion_stats(tasks): ...</code></pre>
          <ul>
            <li><code class="inline">mark_done</code> sets <code class="inline">done</code> to <code class="inline">True</code> for the matching task title.</li>
            <li><code class="inline">completion_stats</code> returns <code class="inline">(total_tasks, completed_tasks, percentage)</code>.</li>
          </ul>

          <p class="sub-title">3. Filtering &amp; display</p>
          <ul>
            <li>Show:
              <ul>
                <li>all tasks,</li>
                <li>only completed tasks,</li>
                <li>only pending tasks.</li>
              </ul>
            </li>
          </ul>
          <p>Use aligned printing, for example:</p>
          <pre><code>Title               Category     Status
-----------------------------------------
Study Python        study        DONE
Clean room          personal     TODO</code></pre>

          <p class="sub-title">4. Saving &amp; loading</p>
          <ul>
            <li>Save all tasks to <code class="inline">"tasks.txt"</code>.</li>
            <li>Load them back and restore the <code class="inline">tasks</code> list.</li>
          </ul>

          <p class="sub-title">5. Menu system</p>
          <pre><code>1. Add task
2. Mark task as done
3. Show all tasks
4. Show tasks by category
5. Show completion stats
6. Save tasks
7. Load tasks
8. Exit</code></pre>

          <p class="sub-title">6. Bonus</p>
          <ul>
            <li>Allow deleting a task by title.</li>
            <li>Count how many tasks per category (dict of category → count).</li>
          </ul>
        </div>
      </article>

      <!-- CHALLENGE 5 -->
      <article class="challenge-card">
        <div class="challenge-header">
          <div>
            <div class="challenge-tag">Challenge 5</div>
            <h2 class="challenge-title">Quiz &amp; Grading Engine</h2>
          </div>
          <div class="pill">Logic · Dicts · Files</div>
        </div>
        <div class="challenge-body">
          <p><span class="accent-chip">Goal:</span> Build a quiz system that asks questions, checks answers, scores the user, and saves results.</p>

          <p class="sub-title">Data model</p>
          <p>Use a list of dictionaries for questions:</p>
          <pre><code>questions = [
    {"text": "What is the output of 2 ** 3 in Python?", "answer": "8"},
]</code></pre>

          <p class="sub-title">1. Defining the quiz</p>
          <ul>
            <li>Hard-code at least <strong>10 questions</strong>.</li>
            <li>Include questions about:
              <ul>
                <li>variables and types,</li>
                <li>conditionals,</li>
                <li>loops,</li>
                <li>lists/dicts,</li>
                <li>string methods.</li>
              </ul>
            </li>
            <li>Some questions can be multiple choice (A/B/C/D), others free text.</li>
          </ul>

          <p class="sub-title">2. Running the quiz</p>
          <ul>
            <li>Ask each question in turn and read the user’s answer.</li>
            <li>Compare with the correct answer:
              <ul>
                <li>for text answers, compare lowercased and stripped.</li>
              </ul>
            </li>
            <li>Keep track of:
              <ul>
                <li>number of correct answers,</li>
                <li>number of questions.</li>
              </ul>
            </li>
          </ul>

          <p class="sub-title">3. Scoring &amp; grading</p>
          <ul>
            <li>Compute a score in percentage.</li>
            <li>Use a grading scale:
              <ul>
                <li>&ge; 90 → <code class="inline">"A"</code></li>
                <li>&ge; 80 → <code class="inline">"B"</code></li>
                <li>&ge; 70 → <code class="inline">"C"</code></li>
                <li>otherwise → <code class="inline">"Fail"</code></li>
              </ul>
            </li>
            <li>Show a summary, for example:</li>
          </ul>
          <pre><code>Correct: 7 / 10
Score  : 70.0 %
Grade  : C</code></pre>

          <p class="sub-title">4. Detailed feedback</p>
          <ul>
            <li>After the quiz, print a list of:
              <ul>
                <li>questions the user got wrong,</li>
                <li>the user’s answer,</li>
                <li>the correct answer.</li>
              </ul>
            </li>
          </ul>

          <p class="sub-title">5. Saving results</p>
          <ul>
            <li>Save a report to <code class="inline">"results.txt"</code> containing:
              <ul>
                <li>score and grade,</li>
                <li>number of correct and wrong answers,</li>
                <li>optionally a date/time or run label.</li>
              </ul>
            </li>
          </ul>

          <p class="sub-title">6. Bonus</p>
          <ul>
            <li>Allow the user to choose quiz length (e.g. 5 or 10 questions).</li>
            <li>Change the order of questions by rearranging the list.</li>
          </ul>
        </div>
      </article>

    </section>

    <hr class="divider">

    <footer>
      Python 101 · Project Challenges 
    </footer>
  </main>
</body>
</html>

---

## 📂 Projects Overview

### 1️⃣ Student Management & Grade Analytics
A console-based application to manage student records and perform academic analysis.

**Main functionalities:**
- Add, validate, and store student data
- Compute average grades
- Identify top-performing and failing students
- Group and sort students by criteria
- Display formatted summaries
- Save and reload data using files

---

### 2️⃣ Text Analysis & Word Frequency Tool
A lightweight text analytics tool for processing paragraphs or text files.

**Main functionalities:**
- Text cleaning and normalization
- Word frequency computation
- Top-N word analysis
- Linguistic statistics (vowels, word length, uniqueness)
- Automatic generation of an analysis report

---

### 3️⃣ Expense Tracker with Persistent Storage
A personal finance tracker built as a CLI application.

**Main functionalities:**
- Record expenses with categories, dates, and notes
- Calculate total and per-category spending
- Identify the highest expense
- Filter expenses by criteria
- Persist data using file storage

---

### 4️⃣ To-Do & Habit Tracker
A task and habit management system focused on productivity tracking.

**Main functionalities:**
- Create and categorize tasks
- Mark tasks as completed
- Filter tasks (pending, completed, by category)
- Generate completion statistics
- Save and restore task history

---

### 5️⃣ Quiz & Grading Engine
An interactive quiz system with automated scoring and feedback.

**Main functionalities:**
- Multiple-choice and free-text questions
- Automatic answer validation
- Score calculation and grading logic
- Detailed feedback for incorrect answers
- Export quiz results to a report file

---

## 🛠️ Technologies & Tools
- **Python 3**
- Standard Python library only
- Command Line Interface (CLI)
- No external dependencies

---

## ▶️ How to Run a Project
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/python-mini-projects.git
   ```

2. Navigate to the desired project folder:
   ```bash
   cd python-mini-projects/project-name
   ```

3. Run the script:
    ```bash
    python main.py
    ```

## 🎯 Learning Outcomes

By completing these projects, you will:
  - Gain confidence with Python fundamentals
  - Learn how to structure small applications
  - Understand data persistence using files
  - Improve logical thinking and problem-solving skills
  - Build a solid base for advanced topics (Data Science, Machine Learning, Backend Development)


**📧 baali.ghizlane2@gmail.com**
