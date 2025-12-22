#!/usr/bin/env python3
# quiz_flask_app.py
# UI claire, moderne (style carte centrale + bleu)
# - QUESTIONS & logique identiques
# - Sauvegarde dans /mnt/data/results.txt

from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, flash, send_file
from datetime import datetime
import random, os, json

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-random-key"

RESULTS_PATH = os.path.join('/mnt/data', 'results.txt')
UPLOADED_HTML_PATH = '/mnt/data/PyChallenges.html'

# ---------------- Questions ----------------
QUESTIONS = [
    {"id": 1, "text": "What is the output of 2 ** 3?", "answer": "8", "type": "text"},
    {"id": 2, "text": "Which type is returned by input() ?", "answer": "string", "type": "text"},
    {"id": 3, "text": "What keyword starts a loop in Python?", "choices": ["loop", "for", "repeat"], "answer": "for", "type": "mc"},
    {"id": 4, "text": "What method converts text to lowercase?", "choices": ["lower()", "down()", "small()"], "answer": "lower()", "type": "mc"},
    {"id": 5, "text": "Which structure uses key/value pairs?", "choices": ["list", "dict", "tuple"], "answer": "dict", "type": "mc"},
    {"id": 6, "text": "What is the index of the first element in a list?", "answer": "0", "type": "text"},
    {"id": 7, "text": "What keyword is used for conditions?", "choices": ["if", "cond", "check"], "answer": "if", "type": "mc"},
    {"id": 8, "text": "len('Python') returns:", "answer": "6", "type": "text"},
    {"id": 9, "text": "What operator tests equality?", "answer": "==", "type": "text"},
    {"id": 10, "text": "What loop repeats while a condition is true?", "answer": "while", "type": "text"},
]

# ---------------- Templates ----------------
# PAGE D’ACCUEIL – thème bleu

INDEX_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Python Quiz — Start</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg-1:#e0f2fe;          /* bleu très clair */
  --bg-2:#eff6ff;          /* bleu/gris clair */
  --card:#ffffff;
  --muted:#6b7280;
  --accent:#0f62fe;        /* bleu principal */
  --accent-soft:#06b6d4;   /* turquoise */
  --btn-grad:linear-gradient(90deg,#0f62fe,#06b6d4);
  --shadow:0 18px 45px rgba(15,23,42,0.12);
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  margin:0;
  background:linear-gradient(180deg,var(--bg-1) 0%,var(--bg-2) 100%);
  font-family:Inter,system-ui,Arial;
  color:#020617;
  -webkit-font-smoothing:antialiased;
}
.page{
  min-height:100vh;
  padding:40px 16px 48px;
  display:flex;
  align-items:center;
  justify-content:center;
}
.container{
  max-width:880px;
  width:100%;
  text-align:center;
}

/* logo SVG moderne */
.logo-wrapper{
  width:96px;
  height:96px;
  margin:0 auto 18px;
}
.logo-icon{
  width:100%;
  height:100%;
  filter:drop-shadow(0 18px 45px rgba(37,99,235,0.45));
}

/* titres */
h1{
  font-size:40px;
  font-weight:700;
  letter-spacing:0.02em;
  color:#0f172a;
}
.subtitle{
  margin-top:10px;
  font-size:16px;
  color:#4b5563;
}

/* carte centrale */
.card{
  margin:40px auto 0;
  max-width:520px;
  background:var(--card);
  padding:28px 28px 26px;
  border-radius:24px;
  box-shadow:var(--shadow);
  border:1px solid #e5e7eb;
  text-align:left;
}
.card-title{
  text-align:center;
  font-size:15px;
  font-weight:600;
  color:#1d4ed8;
  margin-bottom:22px;
}

/* ligne select */
.field-row{
  display:flex;
  align-items:center;
  justify-content:center;
}

/* input nombre questions */
.select-wrapper{
  border-radius:999px;
  border:1px solid #e5e7eb;
  background:#f9fafb;
  padding:8px 14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  min-width:140px;
}
select{
  border:none;
  outline:none;
  background:transparent;
  font-size:14px;
  color:#111827;
}
.select-max{
  font-size:13px;
  color:#9ca3af;
}

/* shuffle */
.shuffle-row{
  margin-top:18px;
  display:flex;
  justify-content:center;
  align-items:center;
  gap:10px;
  font-size:14px;
  color:#4b5563;
}
.shuffle-row input[type="checkbox"]{
  width:18px;
  height:18px;
}

/* bouton */
.actions{
  margin-top:22px;
  text-align:center;
}
.btn-primary{
  border:none;
  border-radius:999px;
  padding:12px 30px;
  font-weight:600;
  font-size:15px;
  color:white;
  cursor:pointer;
  background:var(--btn-grad);
  box-shadow:0 14px 30px rgba(37,99,235,0.45);
}
.btn-primary span{
  margin-left:6px;
}

/* lien tentatives */
.history-link{
  margin-top:12px;
  font-size:13px;
  color:#1d4ed8;
  text-decoration:none;
  display:block;
  text-align:center;
}
.history-link:hover{ text-decoration:underline; }

@media (max-width:640px){
  h1{font-size:32px;}
  .card{margin-top:28px;padding:22px 18px;}
}
</style>
</head>
<body>
  <div class="page">
    <div class="container">
      <!-- Nouveau logo SVG -->
      <div class="logo-wrapper">
        <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" class="logo-icon">
          <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0F62FE"/>
              <stop offset="100%" stop-color="#06B6D4"/>
            </linearGradient>
          </defs>

          <!-- carré arrondi -->
          <rect x="10" y="10" width="180" height="180" rx="40" fill="url(#grad1)" />

          <!-- icône snake Python minimaliste -->
          <path d="M100 55c-22 0-35 12-35 30v20c0 10 8 18 18 18h30c10 0 17 7 17 17v18c0 20-13 32-35 32"
                stroke="white" stroke-width="12" fill="none" stroke-linecap="round"/>
          <circle cx="120" cy="75" r="8" fill="white"/>
        </svg>
      </div>

      <h1>Python Quiz Engine</h1>
      <p class="subtitle">Practice and assess your Python skills in minutes.</p>

      <form method="get" action="{{ url_for('quiz') }}">
        <div class="card">
          <div class="card-title">Number of Questions</div>

          <div class="field-row">
            <div class="select-wrapper">
              <select name="n">
                <option value="5">5</option>
                <option value="10" selected>10</option>
              </select>
              <span class="select-max">/ 10</span>
            </div>
          </div>

          <label class="shuffle-row">
            <input type="checkbox" name="shuffle" checked>
            <span>Shuffle Questions</span>
          </label>

          <div class="actions">
            <button type="submit" class="btn-primary">
              Start Quiz <span>›</span>
            </button>
          </div>

          <a href="{{ url_for('history') }}" class="history-link">View attempts history</a>
        </div>
      </form>
    </div>
  </div>
</body>
</html>
"""

# QUIZ – fond clair bleu, carte blanche
QUIZ_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz — Question</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg-1:#e0f2fe;
  --bg-2:#eff6ff;
  --card:#ffffff;
  --muted:#6b7280;
  --accent-a:#0f62fe;
  --accent-b:#06b6d4;
  --soft:#e0f2fe;
  --shadow:0 18px 45px rgba(15,23,42,0.10);
}
*{box-sizing:border-box}
body{
  margin:0;
  background:linear-gradient(180deg,var(--bg-1) 0%,var(--bg-2) 100%);
  font-family:Poppins,Inter,Arial;
  color:#020617;
  padding:28px 16px;
}
.center{display:flex;justify-content:center}
.container{width:700px;max-width:100%}
.card{
  background:var(--card);
  border-radius:22px;
  padding:26px 26px 24px;
  box-shadow:var(--shadow);
  border:1px solid #e5e7eb;
}
.top-row{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:14px;
  color:var(--muted);
  font-size:13px;
}
.progress{
  height:10px;
  border-radius:999px;
  background:#e5e7eb;
  overflow:hidden;
}
.progress i{
  display:block;
  height:100%;
  width:0%;
  background:linear-gradient(90deg,var(--accent-a),var(--accent-b));
  transition:width .4s ease;
}
.qbox{
  background:var(--soft);
  border-radius:16px;
  padding:22px;
  border:1px solid #e5e7eb;
  margin-top:18px;
}
.qtitle{
  font-size:20px;
  font-weight:600;
  margin-bottom:16px;
}
.choice{
  background:#ffffff;
  border-radius:12px;
  padding:12px 14px;
  border:1px solid #e5e7eb;
  margin-bottom:10px;
  display:flex;
  align-items:center;
  gap:10px;
  cursor:pointer;
  font-size:14px;
}
.choice:hover{
  box-shadow:0 10px 25px rgba(148,163,184,0.35);
  transform:translateY(-2px);
  transition:all .15s ease;
}
.choice input{margin-right:4px;}
input[type="text"]{
  width:100%;
  padding:11px 12px;
  border-radius:12px;
  border:1px solid #bae6fd;
  font-size:14px;
}
.actions{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top:20px;
}
.btn{
  background:linear-gradient(90deg,var(--accent-a),var(--accent-b));
  color:white;
  padding:10px 20px;
  border-radius:999px;
  border:none;
  font-weight:600;
  font-size:14px;
  cursor:pointer;
}
.btn-ghost{
  background:transparent;
  border:1px solid #e5e7eb;
  padding:9px 16px;
  border-radius:999px;
  color:var(--muted);
  font-size:13px;
  text-decoration:none;
}
@media (max-width:640px){
  .card{padding:20px 16px;}
}
</style>
</head>
<body>
  <div class="center">
    <div class="container">
      <div class="card">
        <div class="top-row">
          <div>Question <span id="qIndex">1</span> of {{ total }}</div>
          <div id="percent">0%</div>
        </div>
        <div class="progress" aria-hidden="true"><i id="progBar"></i></div>

        <form id="quizForm" method="post" action="{{ url_for('submit') }}">
          {% for q in questions %}
            <div class="qbox" data-qid="{{ q.id }}" style="display:none">
              <div class="qtitle">{{ loop.index }}. {{ q.text }}</div>

              {% if q.type == 'mc' %}
                {% for c in q.choices %}
                  <label class="choice">
                    <input type="radio" name="q{{q.id}}" value="{{c}}">
                    <div style="flex:1">{{ c }}</div>
                  </label>
                {% endfor %}
              {% else %}
                <div><input type="text" name="q{{q.id}}" placeholder="Your answer"></div>
              {% endif %}
            </div>
          {% endfor %}

          <input type="hidden" name="ids" value="{{ ids }}">
          <div class="actions">
            <button type="button" id="prev" class="btn-ghost">← Previous</button>
            <div style="display:flex;gap:8px">
              <a class="btn-ghost" href="{{ url_for('index') }}">Cancel</a>
              <button type="button" id="next" class="btn">Next</button>
              <button type="submit" id="submitBtn" class="btn" style="display:none">Submit</button>
            </div>
          </div>
        </form>

      </div>
    </div>
  </div>

<script>
(function(){
  const boxes = Array.from(document.querySelectorAll('.qbox'));
  const total = boxes.length;
  let idx = 0;
  const prog = document.getElementById('progBar');
  const qIndex = document.getElementById('qIndex');
  const percent = document.getElementById('percent');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const submitBtn = document.getElementById('submitBtn');

  function show(i){
    boxes.forEach((b,bi)=> b.style.display = bi===i ? 'block' : 'none');
    const pct = Math.round(((i+1)/total)*100);
    prog.style.width = pct + '%';
    qIndex.textContent = (i+1);
    percent.textContent = pct + '%';
    prev.style.display = i===0 ? 'none' : 'inline-block';
    next.style.display = i === total-1 ? 'none' : 'inline-block';
    submitBtn.style.display = i === total-1 ? 'inline-block' : 'none';
    window.scrollTo({top:0,behavior:'smooth'});
  }

  prev.addEventListener('click', ()=>{ if(idx>0){ idx--; show(idx);} });
  next.addEventListener('click', ()=>{
    const cur = boxes[idx];
    const inputs = Array.from(cur.querySelectorAll('input[type=text], input[type=radio]'));
    let answered = false;
    inputs.forEach(i=>{
      if(i.type==='text' && i.value.trim()!=='') answered = true;
      if(i.type==='radio' && i.checked) answered = true;
    });
    if(!answered){ if(!confirm('No answer entered. Continue?')) return; }
    if(idx < total-1){ idx++; show(idx); }
  });

  document.addEventListener('keydown', (e)=>{
    if(e.key==='ArrowRight') next.click();
    if(e.key==='ArrowLeft') prev.click();
  });

  show(0);
})();
</script>
</body>
</html>
"""

RESULTS_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz Results</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg-1:#e0f2fe;
  --bg-2:#eff6ff;
  --card:#ffffff;
  --muted:#6b7280;
  --accent-a:#0f62fe;
  --accent-b:#06b6d4;
  --good:#e6ffef;
  --bad:#fff1f0;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:linear-gradient(180deg,var(--bg-1) 0%,var(--bg-2) 100%);
  font-family:Poppins,Inter,Arial;
  color:#020617;
  padding:32px 16px;
}
.center{display:flex;justify-content:center}
.container{width:720px;max-width:100%}
.card{
  background:var(--card);
  border-radius:24px;
  padding:30px 30px 26px;
  box-shadow:0 18px 45px rgba(15,23,42,0.1);
  border:1px solid #e5e7eb;
}
.header{text-align:center;margin-bottom:18px}
.big-grade{font-size:40px;font-weight:800;margin:6px 0}
.percent{font-size:22px;color:var(--muted);margin-bottom:6px}
.summary-meta{color:var(--muted)}
.feedback{max-height:360px;overflow:auto;margin-top:18px;padding-right:6px}
.item{border-radius:14px;padding:14px 14px 12px;margin-bottom:10px;border:1px solid #f0f0f0}
.item.good{background:var(--good);border-color:#c6f3d7}
.item.bad{background:var(--bad);border-color:#f8d7da}
.item strong{display:block;margin-bottom:6px}
.actions{display:flex;justify-content:space-between;align-items:center;margin-top:18px;gap:12px}
.btn{background:linear-gradient(90deg,var(--accent-a),var(--accent-b));color:white;padding:11px 18px;border-radius:999px;border:none;font-weight:600;cursor:pointer;font-size:14px}
.btn-ghost{background:transparent;border:1px solid #e5e7eb;padding:10px 16px;border-radius:999px;color:var(--muted);font-size:13px;text-decoration:none}
.small{color:var(--muted);font-size:13px}
@media (max-width:640px){
  .container{width:100%}
  .actions{flex-direction:column;align-items:stretch}
  .btn,.btn-ghost{text-align:center;width:100%}
}
</style>
</head>
<body>
  <div class="center">
    <div class="container">
      <div class="card">
        <div class="header">
          <div style="font-size:20px;color:#0f172a;font-weight:700">Quiz Complete!</div>
          <div class="big-grade" style="color: {% if score >= 70 %}#16a34a{% else %}#dc2626{% endif %}">{{ grade }}</div>
          <div class="percent">{{ score }}%</div>
          <div class="summary-meta">Correct: <strong>{{ correct }} / {{ total }}</strong></div>
        </div>

        <h3 style="margin-bottom:8px;">Detailed Feedback</h3>
        <div class="feedback">
          {% for w in wrong %}
            <div class="item bad">
              <strong>Q: {{ w.question }}</strong>
              <div class="small">Your answer: <strong>{{ w.given }}</strong></div>
              <div class="small" style="color:#15803d">Correct answer: <strong>{{ w.correct }}</strong></div>
            </div>
          {% endfor %}
          {% if right %}
            {% for r in right %}
              <div class="item good">
                <strong>Q: {{ r.question }}</strong>
                <div class="small" style="color:#15803d">Your answer: <strong>{{ r.given }}</strong></div>
              </div>
            {% endfor %}
          {% endif %}
        </div>

        <div class="actions">
          <a href="{{ url_for('index') }}" class="btn-ghost">Take another quiz</a>
          <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end">
            <button id="download" class="btn">Download results</button>
            <a href="{{ url_for('history') }}" class="btn-ghost">View attempts</a>
          </div>
        </div>

      </div>
    </div>
  </div>

<script>
(function(){
  const payload = {
    timestamp: "{{ timestamp }}",
    score: "{{ score }}",
    grade: "{{ grade }}",
    correct: "{{ correct }}",
    total: "{{ total }}",
    wrong: {{ wrong | tojson }},
    right: {{ right | tojson }}
  };

  document.getElementById('download').addEventListener('click', ()=>{
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'quiz-result.json'; a.click(); URL.revokeObjectURL(url);
  });
})();
</script>
</body>
</html>
"""

HISTORY_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>History</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
body{
  margin:0;
  background:linear-gradient(180deg,#e0f2fe,#eff6ff);
  font-family:Poppins,Arial;
  color:#020617;
  padding:28px 16px;
}
.container{max-width:960px;margin:0 auto}
.card{
  background:white;
  border-radius:18px;
  padding:18px;
  box-shadow:0 18px 45px rgba(15,23,42,0.10);
  color:#0b1220;
  border:1px solid #e5e7eb;
}
.table{width:100%;border-collapse:collapse}
.table th,.table td{
  padding:10px;
  border-bottom:1px solid #f1f5f9;
  text-align:left;
  font-size:13px;
}
.small{color:#6b7280;font-size:13px}
.btn-ghost{
  background:transparent;
  border:1px solid #e5e7eb;
  padding:8px 14px;
  border-radius:999px;
  color:#1f2937;
  text-decoration:none;
  font-size:13px;
}
.actions{margin-top:14px;display:flex;gap:8px}
</style>
</head>
<body>
  <div class="container">
    <h1 style="color:#0f172a;margin-bottom:14px;">Attempts history</h1>
    <div class="card">
      {% if attempts %}
        <table class="table">
          <thead><tr><th>Timestamp</th><th>Score</th><th>Grade</th><th>Correct</th><th>Wrong</th></tr></thead>
          <tbody>
            {% for a in attempts %}
              <tr>
                <td class="small">{{ a.timestamp }}</td>
                <td>{{ a.score }}%</td>
                <td>{{ a.grade }}</td>
                <td>{{ a.correct }}</td>
                <td>{{ a.wrong_count }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      {% else %}
        <p class="small">No attempts yet.</p>
      {% endif %}
    </div>
    <div class="actions">
      <a class="btn-ghost" href="{{ url_for('index') }}">Back</a>
      <a class="btn-ghost" href="{{ url_for('download_results_file') }}">Download raw results.txt</a>
    </div>
  </div>
</body>
</html>
"""

# ---------------- Helpers ----------------
def append_result_record(score, grade, correct, total, wrong_details, right_details):
    timestamp = datetime.utcnow().isoformat() + 'Z'
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    record = {
        "timestamp": timestamp,
        "score": score,
        "grade": grade,
        "correct": correct,
        "total": total,
        "wrong": wrong_details,
        "right": right_details
    }
    with open(RESULTS_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\\n")
    return timestamp

def read_attempts():
    if not os.path.exists(RESULTS_PATH):
        return []
    attempts = []
    with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                attempts.append({
                    "timestamp": rec.get("timestamp",""),
                    "score": rec.get("score",""),
                    "grade": rec.get("grade",""),
                    "correct": f'{rec.get("correct",0)}/{rec.get("total",0)}',
                    "wrong_count": len(rec.get("wrong",[]))
                })
            except:
                continue
    attempts.reverse()
    return attempts

# ---------------- Routes ----------------
@app.route('/')
def index():
    return render_template_string(INDEX_HTML, uploaded_path=UPLOADED_HTML_PATH)

@app.route('/quiz', methods=['GET'])
def quiz():
    try:
        n = int(request.args.get('n', 10))
    except:
        n = 10
    shuffle = request.args.get('shuffle') is not None
    pool = QUESTIONS.copy()
    if shuffle:
        random.shuffle(pool)
    selected = pool[:min(n, len(pool))]
    ids = ",".join(str(q['id']) for q in selected)
    return render_template_string(QUIZ_HTML, questions=selected, total=len(selected), ids=ids)

@app.route('/submit', methods=['POST'])
def submit():
    ids = request.form.get('ids','')
    ids_list = [int(x) for x in ids.split(',') if x.strip()]
    correct = 0
    wrong = []
    right = []
    for qid in ids_list:
        q = next((x for x in QUESTIONS if x['id'] == qid), None)
        if not q:
            continue
        key = f'q{qid}'
        given = (request.form.get(key) or '').strip()
        given_norm = given.lower().strip()
        correct_ans = str(q['answer']).lower().strip()
        if given_norm == correct_ans:
            correct += 1
            right.append({"question": q['text'], "given": given or "(no answer)", "correct": q['answer']})
        else:
            wrong.append({"question": q['text'], "given": given or "(no answer)", "correct": q['answer']})
    total = len(ids_list)
    score = round((correct / total) * 100, 1) if total else 0.0
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    else:
        grade = 'Fail'

    timestamp = append_result_record(score, grade, correct, total, wrong, right)
    return render_template_string(RESULTS_HTML, correct=correct, total=total, score=score,
                                  grade=grade, wrong=wrong, right=right, timestamp=timestamp)

@app.route('/history')
def history():
    attempts = read_attempts()
    return render_template_string(HISTORY_HTML, attempts=attempts)

@app.route('/download-results-file')
def download_results_file():
    if os.path.exists(RESULTS_PATH):
        return send_file(RESULTS_PATH, as_attachment=True, download_name='results.txt')
    else:
        flash('No results yet.')
        return redirect(url_for('index'))

@app.route('/uploaded-file')
def uploaded_file():
    directory = os.path.dirname(UPLOADED_HTML_PATH)
    filename = os.path.basename(UPLOADED_HTML_PATH)
    if os.path.exists(UPLOADED_HTML_PATH):
        return send_from_directory(directory, filename)
    else:
        flash('Uploaded file not found.')
        return redirect(url_for('index'))

# ---------------- Run ----------------
if __name__ == '__main__':
  app.run(debug=True, port=9000, use_reloader=False)
