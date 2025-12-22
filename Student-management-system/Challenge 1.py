#!/usr/bin/env python3
"""
Student Management — Modern Portfolio-ready single-file Flask app
- Tailwind Play CDN + Heroicons for modern look
- Add / edit / remove students in-browser, modal edit, sorting, analytics
- Save / Load from /mnt/data/students.txt
- Exposes local files (challenges + screenshot) via /data/<filename>
Run: python student_portfolio_modern.py
Open: http://127.0.0.1:5000
"""
from flask import Flask, render_template_string, request, redirect, url_for, send_file, jsonify, abort
from pathlib import Path
import csv, io, datetime

APP = Flask(__name__)
DATA_DIR = Path("/mnt/data")
DATA_FILE = DATA_DIR / "students.txt"
CHALLENGES_FILE = DATA_DIR / "PyChallenges.html"
SCREENSHOT_FILE = DATA_DIR / "25b3c605-5737-4d86-91db-a8567fd5374d.png"

students = []

# ---- Helpers ----
def add_student_record(name, age, grade):
    students.append({
        "id": (students[-1]["id"] + 1) if students else 1,
        "name": name.strip(),
        "age": int(age),
        "grade": float(grade)
    })

def average_grade():
    return round(sum(s["grade"] for s in students) / len(students), 2) if students else 0.0

def best_student():
    return max(students, key=lambda s: s["grade"]) if students else None

def failing_students(threshold=10.0):
    return [s for s in students if s["grade"] < threshold]

def group_by_age():
    d = {}
    for s in students:
        d[s["age"]] = d.get(s["age"], 0) + 1
    return dict(sorted(d.items()))

def save_to_file(path=DATA_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for s in students:
            writer.writerow([s["id"], s["name"], s["age"], s["grade"]])

def load_from_file(path=DATA_FILE):
    students.clear()
    if not path.exists():
        return False
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            _id, name, age, grade = row
            students.append({"id": int(_id), "name": name, "age": int(age), "grade": float(grade)})
    return True

# ---- Template (Tailwind + small JS) ----
TEMPLATE = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Student Management — Portfolio</title>

  <!-- Tailwind Play CDN (for prototypes / portfolio demos) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Feather icons -->
  <script src="https://unpkg.com/feather-icons"></script>

  <style>
    /* Base backgrounds & overlay */
    :root{
      --bg-overlay: rgba(3,6,20,0.55);
      --glass-bg: rgba(10,20,35,0.6);
      --muted: #9fb0d6;
    }
    body {
      background: url('/data/challenge_background.jpg') center/cover no-repeat fixed;
      color: #e6eef8;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      background: var(--bg-overlay);
      backdrop-filter: blur(4px);
      z-index: 0;
    }

    /* Light theme overrides */
    .light-theme {
      color: #1f2937;
    }
    .light-theme::before {
      background: rgba(255,255,255,0.45);
    }
    .light-theme .glass { background: rgba(255,255,255,0.9); color: #0b1220; }
    .light-theme .muted { color: #64748b; }
    .light-theme .accent-grad { color: white; }

    .glass { 
      background: var(--glass-bg);
      border: 1px solid rgba(255,255,255,0.04);
      backdrop-filter: blur(8px);
      position: relative;
      z-index: 10;
      transition: transform 220ms ease, box-shadow 220ms ease;
    }
    /* Hover/card micro-animations */
    .glass.card-hover:hover {
      transform: translateY(-6px) scale(1.005);
      box-shadow: 0 20px 40px rgba(2,6,23,0.55);
    }
    .accent-grad { background: linear-gradient(90deg,#06b6d4,#7c3aed); color:white; }
    .muted { color: var(--muted); }
    .card-shadow { box-shadow: 0 10px 30px rgba(2,6,23,0.7); }

    .fade-in { animation: fadeIn 360ms ease both; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px);} to { opacity: 1; transform: none; }}

    input:focus { outline: none; box-shadow: 0 6px 18px rgba(99,102,241,0.12); border-color: rgba(124,58,237,0.5); }

    /* Sparkline */
    #sparkline { width: 100%; height: 48px; display:block; }

    /* accessibility: focus-visible */
    .focus-ring:focus-visible { outline: 3px solid rgba(99,102,241,0.18); outline-offset: 2px; border-radius: 8px; }

    /* responsive tweak */
    @media (max-width: 768px){
      .container { padding-left: 1rem; padding-right: 1rem; }
      h1 { font-size: 1.125rem; }
    }
  </style>
</head>
<body class="min-h-screen antialiased">
  <div class="container mx-auto px-6 py-10 relative">
    <header class="flex items-center justify-between mb-6 fade-in">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 flex items-center justify-center rounded-lg accent-grad shadow-lg" aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" class="opacity-90"><path d="M3 12h18" stroke="white" stroke-width="1.6" stroke-linecap="round"/><path d="M6 6h12M6 18h12" stroke="white" stroke-width="1.6" stroke-linecap="round" opacity="0.8"/></svg>
        </div>
        <div>
          <h1 class="text-2xl font-semibold" data-i18n="title">Student Management</h1>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <a id="exportBtn" href="{{ url_for('export_report') }}" class="px-3 py-2 rounded-md accent-grad text-sm shadow-sm focus-ring" data-i18n="export">Export CSV</a>

        <!-- Theme toggle -->
        <button id="themeToggle" aria-pressed="false" class="ml-3 px-3 py-2 rounded-md border border-white/6 text-sm muted focus-ring" title="Toggle theme">
          <span id="themeIcon" class="inline-flex items-center gap-2"><i data-feather="sun"></i><span class="sr-only">Toggle theme</span></span>
        </button>
      </div>
    </header>

    <!-- Landing hero -->
    <section class="fade-in mb-6">
      <div class="glass card-hover rounded-2xl p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 class="text-xl font-semibold" data-i18n="hero_title">Student Dashboard — Prototype</h2>
          <p class="muted mt-1" data-i18n="hero_desc">A modern demonstration of student management with analytics and export.</p>
        </div>
        <div class="text-right">
          <a href="#app" class="px-4 py-2 rounded-md accent-grad focus-ring" data-i18n="enter">Enter the application</a>
        </div>
      </div>
    </section>

    <main id="app" class="space-y-6">
      <!-- Add / Edit Form -->
      <section class="glass card-hover rounded-xl p-6 mb-6 fade-in" aria-labelledby="form-title">
        <h3 id="form-title" class="sr-only">Add student</h3>
        <form id="studentForm" action="/add" method="post" class="grid grid-cols-1 md:grid-cols-6 gap-3 items-end">
          <div class="md:col-span-3">
            <label class="text-sm muted block mb-1" data-i18n="name">Name</label>
            <input name="name" required class="w-full rounded-md px-3 py-2 bg-transparent border border-white/6 placeholder:text-white/40" placeholder="Ex: Lina" data-i18n-placeholder="ph_name">
          </div>
          <div>
            <label class="text-sm muted block mb-1" data-i18n="age">Age</label>
            <input name="age" type="number" min="0" required class="w-full rounded-md px-3 py-2 bg-transparent border border-white/6" placeholder="18">
          </div>
          <div>
            <label class="text-sm muted block mb-1" data-i18n="grade">Grade</label>
            <input name="grade" step="0.1" type="number" required class="w-full rounded-md px-3 py-2 bg-transparent border border-white/6" placeholder="15.5">
          </div>
          <div class="md:col-span-6 text-right">
            <button type="submit" class="px-4 py-2 rounded-md accent-grad font-medium focus-ring" data-i18n="add">Add</button>
            <a href="{{ url_for('save') }}" class="px-3 py-2 rounded-md border border-white/6 text-sm muted ml-2 focus-ring" data-i18n="save">Save</a>
            <a href="{{ url_for('load') }}" class="px-3 py-2 rounded-md border border-white/6 text-sm muted ml-2 focus-ring" data-i18n="load">Load</a>
          </div>
        </form>
      </section>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Students table -->
        <div class="lg:col-span-2 glass rounded-xl p-4 card-shadow fade-in card-hover" role="region" aria-label="Students">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-lg font-semibold" data-i18n="students">Students</h2>
              <div class="text-sm muted"><span id="studentsCount">{{ students|length }}</span> students · Average: <strong id="avgVal">{{ avg }}</strong></div>
            </div>
            <div class="flex items-center gap-2">
              <a class="px-3 py-2 rounded-md border border-white/6 text-sm muted" href="{{ url_for('sorted_by_grade') }}" data-i18n="sort_grade">Sort by grade ↓</a>
              <a class="px-3 py-2 rounded-md border border-white/6 text-sm muted" href="{{ url_for('sorted_by_name') }}" data-i18n="sort_name">Sort by name A→Z</a>
              <a class="px-3 py-2 rounded-md border border-red-600/20 text-sm muted" href="{{ url_for('clear') }}" data-i18n="clear">Clear</a>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead class="text-sm text-white/80">
                <tr class="border-b border-white/6">
                  <th class="py-3 pl-3" data-i18n="name">Name</th>
                  <th data-i18n="age">Age</th>
                  <th data-i18n="grade">Grade</th>
                  <th class="text-right pr-3">Actions</th>
                </tr>
              </thead>
              <tbody id="studentsTableBody">
                {% for s in students %}
                <tr class="odd:bg-white/1/0 even:bg-transparent">
                  <td class="py-3 pl-3">{{ s.name }}</td>
                  <td>{{ s.age }}</td>
                  <td>{{ '%.2f'|format(s.grade) }}</td>
                  <td class="text-right pr-3">
                    <button onclick="openEdit({{ loop.index0 }})" class="text-sm px-3 py-1 rounded-md border border-white/6 mr-2">Edit</button>
                    <a href="/remove/{{ loop.index0 }}" class="text-sm px-3 py-1 rounded-md border border-red-600/30 text-red-400">Delete</a>
                  </td>
                </tr>
                {% else %}
                <tr><td colspan="4" class="py-6 muted text-center" data-i18n="no_students">No students yet — add one above.</td></tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Analytics -->
        <aside class="glass rounded-xl p-4 card-shadow fade-in card-hover" role="region" aria-label="Analytics">
          <h3 class="font-semibold mb-2" data-i18n="analytics">Analytics</h3>

          <div class="mb-4">
            <div class="text-sm muted" data-i18n="best_student">Best student</div>
            {% if best %}
              <div class="mt-1"><strong class="text-cyan-300" id="bestName">{{ best.name }}</strong> — <span id="bestGrade">{{ '%.2f'|format(best.grade) }}</span></div>
            {% else %}
              <div class="muted">—</div>
            {% endif %}
          </div>

          <div class="mb-4">
            <div class="text-sm muted" data-i18n="failing">Failing (threshold 10)</div>
            <ul class="mt-2 list-disc ml-5" id="failingList">
              {% for f in failing %}
                <li>{{ f.name }} ({{ '%.2f'|format(f.grade) }})</li>
              {% else %}
                <li class="muted">None</li>
              {% endfor %}
            </ul>
          </div>

          <div class="mb-3">
            <div class="text-sm muted" data-i18n="group_by_age">Group by age</div>
            <ul class="mt-2 ml-5" id="groupByAgeList">
              {% for age,count in grouped.items() %}
                <li>{{ age }} years : {{ count }}</li>
              {% else %}
                <li class="muted">—</li>
              {% endfor %}
            </ul>
          </div>

          <div class="mt-4">
            <div class="text-sm muted mb-1">Grades sparkline (recent)</div>
            <svg id="sparkline" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true"></svg>
          </div>
        </aside>
      </div>

    </main>

    <!-- Edit modal (hidden) -->
    <div id="editModal" class="fixed inset-0 bg-black/50 hidden items-center justify-center z-50">
      <div class="bg-slate-900 rounded-xl p-6 w-full max-w-xl glass">
        <h3 class="text-lg font-semibold mb-4" data-i18n="edit_student">Edit student</h3>
        <form id="editForm" method="post">
          <input type="hidden" name="index" id="editIndex">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label class="text-sm muted block mb-1" data-i18n="name">Name</label>
              <input id="editName" name="name" required class="w-full rounded-md px-3 py-2 bg-transparent border border-white/6">
            </div>
            <div>
              <label class="text-sm muted block mb-1" data-i18n="age">Age</label>
              <input id="editAge" name="age" type="number" required class="w-full rounded-md px-3 py-2 bg-transparent border border-white/6">
            </div>
            <div>
              <label class="text-sm muted block mb-1" data-i18n="grade">Grade</label>
              <input id="editGrade" name="grade" type="number" step="0.1" required class="w-full rounded-md px-3 py-2 bg-transparent border border-white/6">
            </div>
          </div>
          <div class="mt-4 text-right">
            <button type="button" onclick="closeEdit()" class="px-3 py-2 rounded-md border border-white/6 mr-2" data-i18n="cancel">Cancel</button>
            <button type="submit" class="px-4 py-2 rounded-md accent-grad" data-i18n="save_btn">Save</button>
          </div>
        </form>
      </div>
    </div>

    <script>
    // Translations (simple)
    const TRANSLATIONS = {
      en: {
        title: 'Student Management',
        export: 'Export CSV',
        hero_title: 'Student Dashboard — Prototype',
        hero_desc: 'A modern demonstration of student management with analytics and export.',
        enter: 'Enter the application',
        name: 'Name',
        age: 'Age',
        grade: 'Grade',
        ph_name: 'Ex: Lina',
        add: 'Add',
        save: 'Save',
        load: 'Load',
        students: 'Students',
        sort_grade: 'Sort by grade ↓',
        sort_name: 'Sort by name A→Z',
        clear: 'Clear',
        no_students: 'No students yet — add one above.',
        analytics: 'Analytics',
        best_student: 'Best student',
        failing: 'Failing (threshold 10)',
        group_by_age: 'Group by age',
        edit_student: 'Edit student',
        cancel: 'Cancel',
        save_btn: 'Save'
      },
      fr: {
        title: 'Student Management',
        export: 'Exporter CSV',
        hero_title: 'Dashboard étudiant — Prototype',
        hero_desc: "Une démonstration moderne de gestion d'étudiants avec analytics et export.",
        enter: "Entrer dans l'application",
        name: 'Nom',
        age: 'Âge',
        grade: 'Note',
        ph_name: 'Ex: Lina',
        add: 'Ajouter',
        save: 'Sauvegarder',
        load: 'Charger',
        students: 'Étudiants',
        sort_grade: 'Trier par note ↓',
        sort_name: 'Trier par nom A→Z',
        clear: 'Vider',
        no_students: "Aucun étudiant pour l'instant — ajoute en un.",
        analytics: 'Analytics',
        best_student: 'Meilleur étudiant',
        failing: 'En échec (seuil 10)',
        group_by_age: 'Groupe par âge',
        edit_student: 'Modifier étudiant',
        cancel: 'Annuler',
        save_btn: 'Enregistrer'
      }
    };

    function applyLang(lang){
      document.querySelectorAll('[data-i18n]').forEach(el=>{
        const key = el.dataset.i18n;
        const text = TRANSLATIONS[lang] && TRANSLATIONS[lang][key];
        if(text !== undefined) el.textContent = text;
      });
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{
        const key = el.dataset.i18nPlaceholder;
        const text = TRANSLATIONS[lang] && TRANSLATIONS[lang][key];
        if(text !== undefined) el.placeholder = text;
      });
      localStorage.setItem('lang', lang);
    }

    // Theme toggle
    const themeBtn = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');

    function setTheme(isLight){
      const body = document.documentElement;
      if(isLight){
        body.classList.add('light-theme');
        themeBtn.setAttribute('aria-pressed','true');
        themeIcon.innerHTML = '<i data-feather="moon"></i>';
      } else {
        body.classList.remove('light-theme');
        themeBtn.setAttribute('aria-pressed','false');
        themeIcon.innerHTML = '<i data-feather="sun"></i>';
      }
      feather.replace();
      localStorage.setItem('themeLight', isLight ? '1' : '0');
    }
    themeBtn.addEventListener('click', ()=>{
      const current = localStorage.getItem('themeLight') === '1';
      setTheme(!current);
    });

    // Sparkline drawing (small, client-side)
    function drawSparkline(grades){
      const svg = document.getElementById('sparkline');
      if(!svg) return;
      const w = 100, h = 30;
      svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
      if(!grades || grades.length === 0){
        svg.innerHTML = '<text x="50" y="18" text-anchor="middle" fill="rgba(255,255,255,0.35)" font-size="8">No data</text>';
        return;
      }
      // use last N grades
      const N = Math.min(20, grades.length);
      const arr = grades.slice(-N);
      const max = Math.max(...arr), min = Math.min(...arr);
      const range = (max - min) || 1;
      const step = w / (N - 1 || 1);
      let path = '';
      arr.forEach((g, i) => {
        const x = i * step;
        const y = h - ((g - min) / range) * (h - 6) - 3;
        path += (i===0 ? `M ${x} ${y}` : ` L ${x} ${y}`);
      });
      // build gradient + stroke
      svg.innerHTML = `
        <defs>
          <linearGradient id="g1" x1="0" x2="1">
            <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.9"/>
          </linearGradient>
        </defs>
        <path d="${path}" fill="none" stroke="url(#g1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
      `;
    }

    // Setup icons & initial UI
    document.addEventListener('DOMContentLoaded', () => {
      // Feather icons
      feather.replace();

      // initialize theme from localStorage
      const storedTheme = localStorage.getItem('themeLight') === '1';
      setTheme(storedTheme);

      // initial language
      const storedLang = localStorage.getItem('lang') || 'en';
      applyLang(storedLang);

      // wire sample language toggles if present (not visible by default)
      const le = document.getElementById('lang-en');
      const lf = document.getElementById('lang-fr');
      if(le) le.addEventListener('click', ()=> applyLang('en'));
      if(lf) lf.addEventListener('click', ()=> applyLang('fr'));

      // draw sparkline using data rendered server-side
      const grades = {{ students | map(attribute='grade') | list | tojson }};
      drawSparkline(grades);

      // expose a small helper to update UI when server changes (if you want to call client-side)
      window._updateUi = function(){
        document.getElementById('avgVal').textContent = '{{ avg }}';
        const g = {{ students | map(attribute='grade') | list | tojson }};
        drawSparkline(g);
      };
    });

    // Edit modal logic
    const students = {{ students | tojson }};
    function openEdit(index) {
      const s = students[index];
      if(!s) return;
      document.getElementById('editIndex').value = index;
      document.getElementById('editName').value = s.name;
      document.getElementById('editAge').value = s.age;
      document.getElementById('editGrade').value = s.grade;
      document.getElementById('editModal').classList.remove('hidden');
      document.getElementById('editModal').classList.add('flex');
      document.getElementById('editForm').action = '/edit/' + index;
    }
    function closeEdit() {
      document.getElementById('editModal').classList.add('hidden');
      document.getElementById('editModal').classList.remove('flex');
    }
    document.getElementById('editModal').addEventListener('click', (e) => {
      if (e.target.id === 'editModal') closeEdit();
    });
    </script>
  </div>
</body>
</html>
"""

# ---- Routes ----
@APP.route("/data/<path:filename>")
def serve_data(filename):
    # Only allow files in /mnt/data
    safe_path = DATA_DIR / filename
    try:
        # prevent path traversal
        if not safe_path.resolve().is_relative_to(DATA_DIR.resolve()):
            abort(404)
    except Exception:
        pass
    if not safe_path.exists():
        abort(404)
    return send_file(safe_path)

@APP.route("/")
def index():
    return render_template_string(
        TEMPLATE,
        students=students,
        avg=average_grade(),
        best=best_student(),
        failing=failing_students(10),
        grouped=group_by_age(),
        challenges_name=CHALLENGES_FILE.name,
        screenshot_name=SCREENSHOT_FILE.name
    )

@APP.route("/add", methods=["POST"])
def add():
    try:
        name = request.form["name"]
        age = int(request.form["age"])
        grade = float(request.form["grade"])
    except Exception:
        return "Invalid input", 400
    add_student_record(name, age, grade)
    return redirect(url_for("index"))

@APP.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    if not (0 <= index < len(students)):
        return "Index out of range", 404
    try:
        name = request.form["name"]
        age = int(request.form["age"])
        grade = float(request.form["grade"])
    except Exception:
        return "Invalid input", 400
    students[index].update({"name": name.strip(), "age": age, "grade": grade})
    return redirect(url_for("index"))

@APP.route("/remove/<int:index>")
def remove(index):
    if 0 <= index < len(students):
        students.pop(index)
    return redirect(url_for("index"))

@APP.route("/save")
def save():
    save_to_file()
    return redirect(url_for("index"))

@APP.route("/load")
def load():
    load_from_file()
    return redirect(url_for("index"))

@APP.route("/clear")
def clear():
    students.clear()
    return redirect(url_for("index"))

@APP.route("/sorted/grade")
def sorted_by_grade():
    students.sort(key=lambda s: s["grade"], reverse=True)
    return redirect(url_for("index"))

@APP.route("/sorted/name")
def sorted_by_name():
    students.sort(key=lambda s: s["name"].lower())
    return redirect(url_for("index"))

@APP.route("/export")
def export_report():
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "name", "age", "grade"])
    for s in students:
        writer.writerow([s["id"], s["name"], s["age"], s["grade"]])
    buf.seek(0)
    filename = f"students_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(io.BytesIO(buf.getvalue().encode("utf-8")), mimetype="text/csv", as_attachment=True, download_name=filename)

if __name__ == "__main__":
    # preload if exists
    load_from_file()
    APP.run(host="0.0.0.0", port=5000, debug=True)
