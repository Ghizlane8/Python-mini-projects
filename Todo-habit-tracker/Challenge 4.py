#!/usr/bin/env python3
# todo_web_app_pro.py
"""
Professional To-Do & Habit Tracker — single-file Flask app
- English UI
- Keeps default categories (study/work/personal/general)
- If a new category is entered, it is added to categories.json and shown in the UI
- Toggle complete / reopen, edit, delete, bulk actions, import/export, backups
Improvements added:
- Toast notifications (success/error) with Undo for Delete
- Client-side validation (title required, max length)
- Accessibility attributes (aria) & keyboard shortcuts (Enter to add, Esc to close modal)
- Focus management for modal
- Header centered & title visually emphasized; status column centered
- Logo removed; title placed inside a framed badge that follows the logo structure
Run:
  python -m pip install flask
  python todo_web_app_pro.py
Open http://127.0.0.1:5000
"""
from __future__ import annotations
from flask import Flask, jsonify, request, send_file, render_template_string
from pathlib import Path
from datetime import datetime
import json, io

APP = Flask(__name__)
APP.config["JSON_SORT_KEYS"] = False

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "tasks.json"
CATS_FILE = APP_DIR / "categories.json"
BACKUP_DIR = APP_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

DEFAULT_CATEGORIES = ["study", "work", "personal", "general"]

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_tasks(tasks: list[dict], make_backup: bool = True) -> None:
    if make_backup and DATA_FILE.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        try:
            (BACKUP_DIR / f"tasks-{stamp}.json").write_text(DATA_FILE.read_text(encoding="utf-8"), encoding="utf-8")
        except Exception:
            pass
    DATA_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

def load_categories() -> list[str]:
    # Return categories from categories.json, or defaults if file missing/invalid
    if CATS_FILE.exists():
        try:
            cats = json.loads(CATS_FILE.read_text(encoding="utf-8"))
            if isinstance(cats, list):
                # normalize to strings
                return [str(c) for c in cats]
        except Exception:
            pass
    return DEFAULT_CATEGORIES.copy()

def save_categories(cats: list[str]) -> None:
    # Save unique, stable-ordered categories
    unique = []
    for c in cats:
        if not c:
            continue
        cstr = str(c).strip()
        if cstr and cstr not in unique:
            unique.append(cstr)
    try:
        CATS_FILE.write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def ensure_category_exists(cat: str) -> None:
    cat = (cat or "").strip()
    if not cat:
        return
    cats = load_categories()
    if cat not in cats:
        cats.append(cat)
        save_categories(cats)

def find_index(tasks: list[dict], title: str) -> int:
    tn = title.strip().lower()
    for i, t in enumerate(tasks):
        if t.get("title","").strip().lower() == tn:
            return i
    return -1

def merged_categories_from_tasks_and_file(tasks: list[dict]) -> list[str]:
    # keep file categories, but also include any categories currently used by tasks
    file_cats = load_categories()
    seen = set(file_cats)
    merged = file_cats.copy()
    for t in tasks:
        c = (t.get("category") or "").strip()
        if c and c not in seen:
            merged.append(c)
            seen.add(c)
    return merged

# --- API ---
@APP.get("/api/tasks")
def api_get_tasks():
    return jsonify(load_tasks())

@APP.post("/api/tasks")
def api_add_task():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    category = (payload.get("category") or "general").strip()
    if not title:
        return jsonify({"error":"title required"}), 400
    tasks = load_tasks()
    if find_index(tasks, title) != -1:
        return jsonify({"error":"task already exists"}), 400
    # ensure category present in categories list (persist)
    ensure_category_exists(category)
    tasks.append({"title": title, "category": category, "done": False, "created": now_iso()})
    save_tasks(tasks)
    return jsonify({"ok": True}), 201

@APP.put("/api/tasks/<string:title>")
def api_edit_task(title: str):
    payload = request.get_json(silent=True) or {}
    new_title = payload.get("title","").strip()
    new_category = payload.get("category","").strip()
    tasks = load_tasks()
    idx = find_index(tasks, title)
    if idx == -1:
        return jsonify({"error":"not found"}), 404
    if new_title:
        other = find_index(tasks, new_title)
        if other != -1 and other != idx:
            return jsonify({"error":"duplicate title"}), 400
        tasks[idx]["title"] = new_title
    if new_category:
        tasks[idx]["category"] = new_category
        ensure_category_exists(new_category)
    save_tasks(tasks)
    return jsonify({"ok": True})

@APP.post("/api/tasks/mark")
def api_mark_done():
    """
    Toggle endpoint. Accepts JSON: { "title": "...", "done": true|false }.
    If 'done' omitted, defaults to True (mark done).
    """
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    done_flag = payload.get("done", True)
    if not title:
        return jsonify({"error":"title required"}), 400
    tasks = load_tasks(); idx = find_index(tasks, title)
    if idx == -1:
        return jsonify({"error":"not found"}), 404
    tasks[idx]["done"] = bool(done_flag)
    save_tasks(tasks)
    return jsonify({"ok": True, "title": tasks[idx]["title"], "done": tasks[idx]["done"]})

@APP.post("/api/tasks/mark-bulk")
def api_mark_bulk():
    payload = request.get_json(silent=True) or {}
    titles = payload.get("titles") or []
    done_flag = payload.get("done", True)
    if not isinstance(titles, list):
        return jsonify({"error":"titles must be list"}), 400
    tasks = load_tasks(); changed = 0
    for title in titles:
        idx = find_index(tasks, title)
        if idx != -1 and tasks[idx].get("done", False) != bool(done_flag):
            tasks[idx]["done"] = bool(done_flag); changed += 1
    if changed: save_tasks(tasks)
    return jsonify({"ok": True, "changed": changed})

@APP.delete("/api/tasks/<string:title>")
def api_delete_task(title: str):
    tasks = load_tasks()
    new = [t for t in tasks if t.get("title","").strip().lower() != title.strip().lower()]
    if len(new) == len(tasks):
        return jsonify({"error":"not found"}), 404
    save_tasks(new)
    return jsonify({"ok": True})

@APP.post("/api/import")
def api_import():
    payload = request.get_json(silent=True)
    if not isinstance(payload, list):
        return jsonify({"error":"payload must be a list"}), 400
    tasks = []
    for el in payload:
        if not isinstance(el, dict) or "title" not in el: continue
        title = str(el.get("title","")).strip()
        category = str(el.get("category","general")).strip()
        done = bool(el.get("done", False))
        created = el.get("created") or now_iso()
        tasks.append({"title": title, "category": category, "done": done, "created": created})
        # ensure categories for imported tasks
        ensure_category_exists(category)
    save_tasks(tasks)
    return jsonify({"ok": True, "imported": len(tasks)})

@APP.get("/api/export")
def api_export():
    tasks = load_tasks()
    buf = io.BytesIO(json.dumps(tasks, ensure_ascii=False, indent=2).encode("utf-8"))
    return send_file(buf, mimetype="application/json", as_attachment=True, download_name="tasks-export.json")

@APP.post("/api/clear")
def api_clear_all():
    save_tasks([])
    return jsonify({"ok": True})

@APP.get("/api/categories")
def api_get_categories():
    # merge categories from file + tasks to avoid losing any used category
    tasks = load_tasks()
    cats = merged_categories_from_tasks_and_file(tasks)
    return jsonify(cats)

# --- UI ---
@APP.get("/")
def index():
    # English UI, improved SaaS-like styling
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>To-Do & Habit Tracker — Professional</title>
<!-- Tailwind CDN (no build) -->
<script src="https://cdn.tailwindcss.com"></script>
<style>
body { background: linear-gradient(180deg,#eef6ff 0%,#f8fafc 40%); }
.card { box-shadow: 0 20px 40px rgba(2,6,23,0.08); }
.btn { transition: transform .06s ease, box-shadow .08s ease; }
.btn:active { transform: translateY(1px); }
.modal-backdrop { background: rgba(2,6,23,0.5); }
/* toast */
.toast-container { position: fixed; right: 20px; bottom: 24px; z-index: 1200; display:flex; flex-direction:column; gap:8px; }
.toast { background: white; border-radius:8px; padding:10px 14px; box-shadow: 0 6px 18px rgba(2,6,23,0.12); display:flex; gap:10px; align-items:center; min-width:220px; }
.toast.success { border-left:4px solid #10b981; }
.toast.error { border-left:4px solid #ef4444; }
.toast .action { margin-left:auto; }

/* emphasize header title */
.header-title {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}
.header-sub {
  letter-spacing: 0.02em;
}

/* title framed box (replaces logo) */
.title-frame {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  padding: 10px 18px;
  border-radius: 14px;
  background: linear-gradient(90deg, rgba(59,130,246,0.12), rgba(99,102,241,0.08));
  border: 1px solid rgba(99,102,241,0.12);
  box-shadow: 0 6px 18px rgba(2,6,23,0.04);
}

/* framed badge left small square (structure like old logo) */
.title-badge {
  width:44px;
  height:44px;
  border-radius:10px;
  background: linear-gradient(135deg,#06b6d4,#7c3aed);
  display:flex;
  align-items:center;
  justify-content:center;
  color:white;
  font-weight:800;
  font-size:16px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.08);
}

/* table status styling */
.status-label {
  display:inline-block;
  padding:6px 10px;
  border-radius:999px;
  font-weight:700;
  font-size:12px;
}
.status-todo { background:#e6f4ff; color:#0369a1; }
.status-done { background:#f1f5f9; color:#475569; border: 1px solid #e6eef8; }

/* center the status column content */
.status-col { text-align:center; }

/* center aligned header */
.header-center { text-align:center; }
</style>
</head><body class="antialiased text-slate-900">
<div class="max-w-6xl mx-auto p-8">
  <!-- CENTERED HEADER: logo removed; framed title -->
  <header class="flex flex-col items-center justify-center mb-6 text-center header-center">
    <div class="title-frame mb-3" role="img" aria-label="App title frame">
      <!-- small badge on the left to mirror previous logo structure (but not a logo file) -->
      <div class="title-badge" aria-hidden="true">TD</div>
      <div class="text-left">
        <h1 class="header-title text-slate-900">
          TO-DO &amp; HABIT TRACKER
        </h1>
        <p class="text-sm text-slate-500 mt-1 header-sub">
          Simple • Local • Professional
        </p>
      </div>
    </div>
  </header>

  <main class="card bg-white rounded-2xl p-6">
    <div class="grid lg:grid-cols-3 gap-6">
      <!-- TASKS LIST -->
      <section class="lg:col-span-2" aria-label="Task list">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <div>
            <label class="text-sm text-slate-600 mr-2" for="filter">Filter</label>
            <select id="filter" class="px-3 py-2 rounded-lg border" onchange="render(tasks)" aria-label="Filter status">
              <option value="all">All</option><option value="done">Completed</option><option value="todo">To Do</option>
            </select>
            <label class="ml-4 text-sm text-slate-600" for="filterCategory">Category</label>
            <select id="filterCategory" class="px-3 py-2 rounded-lg border" onchange="render(tasks)" aria-label="Filter category">
              <option value="">All</option>
            </select>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-ghost px-3 py-2 rounded-lg bg-slate-50 border" onclick="loadTasks()" aria-label="Refresh tasks">🔁 Refresh</button>
            <button id="themeToggle" class="btn px-3 py-2 rounded-lg bg-slate-50 border" aria-pressed="false">Dark</button>
          </div>
        </div>

        <div class="overflow-hidden rounded-xl border" role="region" aria-live="polite">
          <table class="w-full text-left" aria-describedby="stats">
            <thead class="bg-gradient-to-r from-sky-600 to-indigo-600 text-white">
              <tr>
                <th class="px-6 py-3">Title</th>
                <th class="px-6 py-3 w-40">Category</th>
                <th class="px-6 py-3 w-28">Status</th>
                <th class="px-6 py-3 w-64">Actions</th>
              </tr>
            </thead>
            <tbody id="tasksBody" class="bg-white"></tbody>
          </table>
        </div>

        <div class="mt-4 text-sm text-slate-600" id="stats">Total visible: 0 — Completed (all): 0</div>
      </section>

      <!-- CONTROLS -->
      <aside class="space-y-4" aria-label="Controls">
        <div class="bg-slate-50 p-4 rounded-lg">
          <h3 class="font-semibold mb-2">New Task</h3>
          <label class="sr-only" for="title">Title</label>
          <input id="title" maxlength="100" placeholder="Ex: Study Python" class="w-full px-3 py-2 rounded-lg border mb-3" aria-required="true" />
          <!-- free input with suggestions; user can type a new category -->
          <label class="sr-only" for="category">Category</label>
          <input list="categories" id="category" placeholder="Category (e.g. study)" class="w-full px-3 py-2 rounded-lg border mb-2" />
          <datalist id="categories"></datalist>
          <div class="flex gap-2">
            <button class="btn btn-primary px-4 py-2 rounded-lg bg-sky-600 text-white" onclick="addTask()" id="addBtn">➕ Add</button>
            <button class="btn px-4 py-2 rounded-lg bg-white border" onclick="clearInputs()">🧹 Clear</button>
          </div>
          <div id="titleError" class="text-sm text-red-600 mt-2 hidden" role="alert"></div>
        </div>

        <div class="bg-slate-50 p-4 rounded-lg">
          <h3 class="font-semibold mb-2">Bulk Actions</h3>
          <div class="flex flex-col gap-2">
            <button class="btn px-4 py-2 rounded-lg bg-red-500 text-white" onclick="clearAll()">✖ Delete all</button>
            <div class="flex gap-2">
              <button class="btn px-3 py-2 rounded-lg bg-white border" onclick="exportJson()">⬇ Export</button>
              <label class="btn px-3 py-2 rounded-lg bg-white border cursor-pointer" aria-label="Import JSON">
                ⬆ Import <input id="importFile" type="file" accept="application/json" class="hidden" onchange="importFile(event)">
              </label>
            </div>
          </div>
        </div>

      </aside>
    </div>
  </main>
</div>

<!-- Edit modal -->
<div id="modal" class="fixed inset-0 hidden items-center justify-center modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="bg-white rounded-xl p-6 w-96 shadow-xl" role="document">
    <h3 id="modalTitle" class="font-semibold mb-3">Edit Task</h3>
    <label class="sr-only" for="editTitle">Edit title</label>
    <input id="editTitle" class="w-full px-3 py-2 rounded-lg border mb-3" />
    <!-- free category input with same datalist -->
    <label class="sr-only" for="editCategory">Edit category</label>
    <input list="categories" id="editCategory" class="w-full px-3 py-2 rounded-lg border mb-4" placeholder="Category (e.g. study)" />
    <div class="flex justify-end gap-2">
      <button class="btn px-3 py-2 rounded-lg bg-white border" onclick="closeModal()">Cancel</button>
      <button class="btn px-3 py-2 rounded-lg bg-sky-600 text-white" onclick="saveEdit()">Save</button>
    </div>
  </div>
</div>

<!-- Toast container -->
<div class="toast-container" id="toastContainer" aria-live="polite" aria-atomic="true"></div>

<script>
let tasks = [];
let editing = null;
let lastDeleted = null; // used for undo restore

// theme toggle persisted (localStorage)
(function(){
  const theme = localStorage.getItem('tw_theme') || 'light';
  applyTheme(theme);
  document.getElementById('themeToggle').textContent = theme==='dark' ? 'Light' : 'Dark';
})();
function applyTheme(t){
  if(t === 'dark'){ document.documentElement.classList.add('dark'); document.documentElement.style.background = '#0b1220'; document.getElementById('themeToggle').setAttribute('aria-pressed','true'); }
  else { document.documentElement.classList.remove('dark'); document.documentElement.style.background = ''; document.getElementById('themeToggle').setAttribute('aria-pressed','false'); }
  localStorage.setItem('tw_theme', t);
}
document.getElementById('themeToggle').addEventListener('click', ()=>{
  const cur = localStorage.getItem('tw_theme') === 'dark' ? 'dark' : 'light';
  const nxt = cur === 'dark' ? 'light' : 'dark';
  applyTheme(nxt);
  document.getElementById('themeToggle').textContent = nxt==='dark'? 'Light':'Dark';
});

// ---------- Toasts ----------
function showToast(message, opts={type:'success', timeout:5000, undo:false, undoCallback:null}) {
  const container = document.getElementById('toastContainer');
  const div = document.createElement('div');
  div.className = 'toast ' + (opts.type === 'error' ? 'error' : 'success');
  div.setAttribute('role','status');
  div.innerHTML = `<div>${escapeHtml(message)}</div>`;
  if(opts.undo && typeof opts.undoCallback === 'function'){
    const act = document.createElement('div');
    act.className = 'action';
    const btn = document.createElement('button');
    btn.className = 'px-3 py-1 rounded bg-sky-600 text-white text-sm';
    btn.textContent = 'Undo';
    btn.onclick = ()=>{ opts.undoCallback(); // call undo
      container.removeChild(div);
    };
    act.appendChild(btn);
    div.appendChild(act);
  }
  container.appendChild(div);
  if(opts.timeout && opts.timeout > 0){
    setTimeout(()=>{ try{ if(container.contains(div)) container.removeChild(div); }catch(e){} }, opts.timeout);
  }
}

// ---------- Data / UI ----------
async function loadTasks(){
  try {
    const res = await fetch('/api/tasks');
    tasks = await res.json();
    updateCategoryDatalist();
    populateFilterCategories();
    render(tasks);
  } catch(e){ showToast('Error: could not load tasks', {type:'error', timeout:3000}); }
}

function updateCategoryDatalist(){
  // fetch categories from server (or derive locally)
  fetch('/api/categories').then(r=>r.json()).then(cats=>{
    const dl = document.getElementById('categories'); dl.innerHTML = '';
    cats.forEach(c=>{
      const opt = document.createElement('option'); opt.value = c; dl.appendChild(opt);
    });
  }).catch(()=>{
    // fallback: derive from tasks
    const dl = document.getElementById('categories'); dl.innerHTML = '';
    const seen = new Set();
    tasks.forEach(t=>{ const c=(t.category||'general').trim(); if(c && !seen.has(c)){ seen.add(c); const opt=document.createElement('option'); opt.value=c; dl.appendChild(opt); }});
  }).finally(()=>{ populateFilterCategories(); });
}

function populateFilterCategories(){
  const sel = document.getElementById('filterCategory');
  sel.innerHTML = '<option value="">All</option>';
  // pull from datalist options
  const dl = document.getElementById('categories');
  const opts = [...dl.options].map(o=>o.value);
  opts.forEach(v=>{
    const o = document.createElement('option'); o.value = v; o.textContent = v; sel.appendChild(o);
  });
}

function clearInputs(){ document.getElementById('title').value=''; document.getElementById('category').value='study'; document.getElementById('titleError').classList.add('hidden'); }
async function addTask(){
  const titleEl = document.getElementById('title');
  const title = titleEl.value.trim();
  const category = (document.getElementById('category').value || 'general').trim();
  // client-side validation
  if(!title){
    const e = document.getElementById('titleError');
    e.textContent = 'Title required';
    e.classList.remove('hidden');
    titleEl.focus();
    return;
  }
  if(title.length > 100){
    const e = document.getElementById('titleError');
    e.textContent = 'Title must be 100 characters or less';
    e.classList.remove('hidden');
    titleEl.focus();
    return;
  }
  document.getElementById('titleError').classList.add('hidden');
  const res = await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'}, body: JSON.stringify({title,category})});
  if(res.ok){ await loadTasks(); clearInputs(); showToast('Task added'); } else { const j=await res.json(); showToast(j.error||'Error adding task', {type:'error'}); }
}

// toggle done
async function toggleDone(title, done){
  await fetch('/api/tasks/mark',{method:'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify({title, done})});
  loadTasks();
}
async function markDone(title){ return toggleDone(title, true); }
async function unmarkDone(title){ return toggleDone(title, false); }

// delete with undo support
async function deleteTask(title){
  if(!confirm('Delete "'+title+'" ?')) return;
  // capture current task object to allow undo
  const tObj = tasks.find(t=>t.title === title);
  lastDeleted = tObj ? JSON.parse(JSON.stringify(tObj)) : null;
  const res = await fetch('/api/tasks/'+encodeURIComponent(title), {method:'DELETE'});
  if(res.ok){
    loadTasks();
    showToast('Task deleted', {undo:true, undoCallback: async ()=>{
      if(lastDeleted){
        // re-add the deleted task (restore original done state)
        await fetch('/api/tasks', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({title: lastDeleted.title, category: lastDeleted.category})});
        // if it was completed before delete, mark it
        if(lastDeleted.done){
          await fetch('/api/tasks/mark', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({title:lastDeleted.title, done:true})});
        }
        await loadTasks();
        showToast('Undo: task restored');
        lastDeleted = null;
      }
    }, timeout:8000});
  } else {
    const j = await res.json();
    showToast(j.error||'Delete error', {type:'error'});
  }
}

function badgeHTML(cat){
  const map = {study:'bg-sky-100 text-sky-700', work:'bg-orange-50 text-orange-700', personal:'bg-emerald-50 text-emerald-700', general:'bg-slate-100 text-slate-700'};
  const cls = map[cat]||'bg-slate-100 text-slate-700';
  return `<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${cls}">${escapeHtml(cat)}</span>`;
}

function render(list){
  const tbody = document.getElementById('tasksBody'); tbody.innerHTML = '';
  const filter = document.getElementById('filter').value; const filterCat = document.getElementById('filterCategory').value;
  let visible = 0;
  (list||tasks).forEach(t=>{
    if(filterCat && filterCat!=='' && t.category!==filterCat) return;
    if(filter==='done' && !t.done) return;
    if(filter==='todo' && t.done) return;
    visible++;
    const tr = document.createElement('tr');
    tr.className = 'border-b';
    const titleTd = document.createElement('td'); titleTd.className='px-6 py-4';
    titleTd.innerHTML = t.done ? `<span class="line-through text-slate-400">${escapeHtml(t.title)}</span>` : `<span class="font-medium">${escapeHtml(t.title)}</span>`;
    tr.appendChild(titleTd);

    const catTd = document.createElement('td'); catTd.className='px-6 py-4'; catTd.innerHTML = badgeHTML(t.category || 'general'); tr.appendChild(catTd);

    // center status column and make label more visible
    const statusTd = document.createElement('td');
    statusTd.className = 'px-6 py-4 status-col';
    if (t.done) {
      statusTd.innerHTML = `<span class="status-label status-done">COMPLETED</span>`;
    } else {
      statusTd.innerHTML = `<span class="status-label status-todo">TO DO</span>`;
    }
    tr.appendChild(statusTd);

    const actionsTd = document.createElement('td'); actionsTd.className='px-6 py-4 flex gap-2';
    if(!t.done){
      const btn = document.createElement('button'); btn.className='px-3 py-1 rounded-lg bg-sky-600 text-white'; btn.textContent='Complete'; btn.onclick = ()=>markDone(t.title); actionsTd.appendChild(btn);
    } else {
      const btn2 = document.createElement('button'); btn2.className='px-3 py-1 rounded-lg bg-gray-200 text-slate-700'; btn2.textContent='Reopen'; btn2.onclick = ()=>unmarkDone(t.title); actionsTd.appendChild(btn2);
    }
    const edit = document.createElement('button'); edit.className='px-3 py-1 rounded-lg bg-white border'; edit.textContent='Edit'; edit.onclick = ()=>openModal(t.title); actionsTd.appendChild(edit);
    const del = document.createElement('button'); del.className='px-3 py-1 rounded-lg bg-white border'; del.textContent='Delete'; del.onclick = ()=>deleteTask(t.title); actionsTd.appendChild(del);

    tr.appendChild(actionsTd); tbody.appendChild(tr);
  });
  const completedAll = (tasks||[]).filter(x=>x.done).length;
  document.getElementById('stats').textContent = `Total visible: ${visible} — Completed (all): ${completedAll}`;
}

// safe escape
function escapeHtml(s){ return (''+s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

// ---------- Modal ----------
function openModal(title){
  editing = title;
  const t = tasks.find(x=>x.title===title);
  if(!t) return showToast('Task not found', {type:'error'});
  const editTitle = document.getElementById('editTitle');
  const editCategory = document.getElementById('editCategory');
  editTitle.value = t.title;
  editCategory.value = t.category || '';
  const modal = document.getElementById('modal');
  modal.classList.remove('hidden'); modal.classList.add('flex');
  // focus management
  setTimeout(()=>editTitle.focus(), 50);
}
function closeModal(){ document.getElementById('modal').classList.add('hidden'); document.getElementById('modal').classList.remove('flex'); editing=null; }

async function saveEdit(){
  const newTitle = document.getElementById('editTitle').value.trim();
  const newCat = (document.getElementById('editCategory').value || 'general').trim();
  if(!newTitle) { showToast('Title required', {type:'error'}); return; }
  const res = await fetch('/api/tasks/'+encodeURIComponent(editing), {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify({title:newTitle, category:newCat})});
  if(res.ok){ closeModal(); loadTasks(); showToast('Task updated'); } else { const j=await res.json(); showToast(j.error||'Error', {type:'error'}); }
}

// bulk actions
async function markVisibleDone(){
  const filter = document.getElementById('filter').value; const filterCat = document.getElementById('filterCategory').value;
  const visible = (tasks||[]).filter(t=>{
    if(filterCat && filterCat!=='' && t.category!==filterCat) return false;
    if(filter==='done' && !t.done) return false;
    if(filter==='todo' && t.done) return false;
    return !t.done;
  }).map(t=>t.title);
  if(visible.length===0) return showToast('No visible tasks to mark', {type:'error'});
  await fetch('/api/tasks/mark-bulk', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({titles: visible, done: true})});
  loadTasks(); showToast('Marked visible tasks as completed');
}
async function unmarkVisible(){
  const filter = document.getElementById('filter').value; const filterCat = document.getElementById('filterCategory').value;
  const visible = (tasks||[]).filter(t=>{
    if(filterCat && filterCat!=='' && t.category!==filterCat) return false;
    if(filter==='done' && !t.done) return false;
    if(filter==='todo' && t.done) return false;
    return t.done; // only currently done items
  }).map(t=>t.title);
  if(visible.length===0) return showToast('No visible tasks to unmark', {type:'error'});
  await fetch('/api/tasks/mark-bulk', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({titles: visible, done: false})});
  loadTasks(); showToast('Unmarked visible tasks');
}

async function clearAll(){ if(!confirm('Delete all tasks? This is irreversible.')) return; await fetch('/api/clear', {method:'POST'}); loadTasks(); showToast('All tasks deleted'); }
function exportJson(){ window.location = '/api/export'; }
function importFile(ev){
  const file = ev.target.files[0]; if(!file) return;
  const reader = new FileReader();
  reader.onload = async function(e){
    try{
      const tasksList = JSON.parse(e.target.result);
      const res = await fetch('/api/import', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(tasksList)});
      if(res.ok){ loadTasks(); showToast('Import OK'); } else { const j=await res.json(); showToast(j.error||'Import error', {type:'error'}); }
    } catch(err){ showToast('Invalid JSON file', {type:'error'}); }
  };
  reader.readAsText(file, 'utf-8');
}

// keyboard support
document.getElementById('title').addEventListener('keydown', function(e){
  if(e.key === 'Enter'){
    e.preventDefault();
    document.getElementById('addBtn').click();
  }
});
document.addEventListener('keydown', function(e){
  if(e.key === 'Escape'){
    // close modal if open
    const modal = document.getElementById('modal');
    if(!modal.classList.contains('hidden')) closeModal();
  }
});

// initial load
loadTasks();
</script>
</body></html>
"""
    return render_template_string(html)

if __name__ == "__main__":
    APP.run(debug=True, port=8000)
