#!/usr/bin/env python3
# flask_text_analyzer.py
from flask import Flask, request, render_template_string, send_from_directory, url_for
from pathlib import Path
import re, unicodedata, io, json, os
from collections import Counter

# chemin local du fichier exemple (déjà uploadé)
SAMPLE_PATH = "/mnt/data/PyChallenges.html"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", os.urandom(24))

# --- TEMPLATE (HTML + CSS + JS) ---
TEMPLATE = """
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Text Analyzer — Professional</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg: #f3f7f9;
    --card-bg: rgba(255,255,255,0.95);
    --text: #0b2b36;
    --muted: #5a6b72;
    --accent: #6d28d9;
    --accent-2: #06b6d4;
    --glass-border: rgba(11,43,54,0.06);
    --radius: 14px;
    --textarea-bg: #e9f1f5;
    --btn-text: white;
    --shadow: 0 8px 30px rgba(2,6,23,0.06);
  }
  [data-theme="dark"]{
    --bg: #0f4b66;
    --card-bg: rgba(255,255,255,0.03);
    --text: #e9f3f8;
    --muted: #b2c7cf;
    --accent: #6d28d9;
    --accent-2: #06b6d4;
    --glass-border: rgba(255,255,255,0.06);
    --textarea-bg: rgba(6,20,30,0.30);
    --btn-text: white;
    --shadow: 0 8px 30px rgba(2,6,23,0.12);
  }

  *{box-sizing:border-box}
  html,body{height:100%;margin:0}
  body{
    font-family:Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    color:var(--text);
    background: var(--bg);
    -webkit-font-smoothing:antialiased;
    padding:22px;
  }

  .wrap{max-width:1200px;margin:0 auto;display:grid;grid-template-columns: 1fr 420px;gap:24px;align-items:start;}
  @media (max-width:1100px){ .wrap{grid-template-columns: 1fr; padding:12px} }

  header{
    grid-column: 1 / -1;
    display:flex;
    justify-content:center;
    align-items:center;
    margin-bottom:18px;
    text-align:center;
    gap:18px;
  }
  .brand{ display:flex;flex-direction:row;align-items:center;gap:14px; }
  .logo{
    width:68px;height:68px;border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    box-shadow: var(--shadow);
    background: linear-gradient(135deg,var(--accent), #8b5cf6);
    color:white;font-family:Fira Code, monospace;font-weight:700;font-size:20px;
  }
  h1{font-size:1.25rem;margin:0;font-weight:700;letter-spacing:0.2px;color:var(--text)}

  .top-controls{ position:absolute; right:30px; top:22px; display:flex; gap:10px; align-items:center; }
  .theme-toggle{ padding:8px 12px; border-radius:10px; border:1px solid rgba(0,0,0,0.06); cursor:pointer; background:transparent; color:var(--text) }

  .card{
    background: var(--card-bg);
    border-radius: var(--radius);
    padding:18px;
    border:1px solid var(--glass-border);
    box-shadow: var(--shadow);
  }

  .panel{ padding:18px;border-radius:12px; }
  label{display:block;font-weight:600;margin-bottom:6px;color:var(--text)}
  textarea{
    width:100%;min-height:260px;border-radius:10px;padding:12px;border:1px solid rgba(0,0,0,0.06);
    background: var(--textarea-bg); color:var(--text); resize:vertical; font-family:Inter, monospace;
    box-shadow: inset 0 1px 0 rgba(0,0,0,0.02);
  }

  .file-drop{
    margin-top:12px;padding:12px;border-radius:10px;border:1px dashed rgba(0,0,0,0.06);
    display:flex;align-items:center;gap:12px;background: rgba(0,0,0,0.01);
  }
  .btn{
    background:linear-gradient(180deg,var(--accent), #7c3aed);
    color:var(--btn-text);border:none;padding:10px 14px;border-radius:10px;font-weight:700;cursor:pointer;
    box-shadow: 0 10px 20px rgba(109,40,217,0.12);
    transition:transform .12s ease, box-shadow .12s ease;
  }
  .btn.secondary{
    background:transparent;border:1px solid rgba(0,0,0,0.06); color:var(--text); box-shadow:none;padding:10px 12px;border-radius:10px;
  }
  .controls{display:flex;gap:10px;align-items:center;margin-top:12px;flex-wrap:wrap}
  .muted{color:var(--muted);font-size:0.95rem}

  .results { position:sticky; top:28px; display:flex;flex-direction:column;gap:12px; }
  .kpi{display:flex;gap:12px;align-items:center;justify-content:space-between;border-radius:10px;padding:12px;background:rgba(0,0,0,0.02);border:1px solid rgba(0,0,0,0.03); }
  .kpi .label{color:var(--muted);font-size:0.85rem}
  .kpi .value{font-weight:700;font-size:1.05rem}

  hr.sep{border:0;border-top:1px solid rgba(0,0,0,0.05);margin:6px 0 14px}

  table{width:100%;border-collapse:collapse;margin-top:6px;font-size:0.95rem}
  th,td{padding:10px 8px;text-align:left;border-bottom:1px solid rgba(0,0,0,0.04)}
  th{color:var(--muted);font-weight:600;font-size:0.85rem}
  tr:nth-child(even){background:rgba(0,0,0,0.01)}

  .empty-note{color:var(--muted);padding:10px;border-radius:8px;background:rgba(0,0,0,0.01);border:1px dashed rgba(0,0,0,0.03)}
  input[type="file"]{display:none}
  .fake-file{ background:rgba(0,0,0,0.02); border-radius:8px;padding:8px 10px;border:1px solid rgba(0,0,0,0.03); display:flex;align-items:center;justify-content:space-between;gap:8px;color:var(--muted) }
  .icon{ width:18px;height:18px;display:inline-block;opacity:0.95;vertical-align:middle }

  /* Toasts */
  .toasts { position:fixed; right:20px; bottom:20px; z-index:2000; display:flex;flex-direction:column; gap:10px; }
  .toast { padding:10px 14px; border-radius:10px; color:white; font-weight:600; box-shadow:0 6px 20px rgba(0,0,0,0.18); min-width:220px; }
  .toast.error{ background:#ef4444; }
  .toast.success{ background:#059669; }
  .toast.info{ background:#2563eb; }

  /* Word cloud container */
  #wordCloudWrap{ margin-top:14px; border-radius:10px; padding:10px; background: rgba(0,0,0,0.02); border:1px solid rgba(0,0,0,0.03) }
  canvas#wordCloud { width:100%; height:220px; display:block; }
  #cloudActions{ display:flex; gap:8px; margin-top:8px; align-items:center }
  #cloudTooltip{
    position:fixed; pointer-events:none; background:rgba(0,0,0,0.75); color:white; padding:6px 8px; border-radius:6px; font-size:0.85rem; display:none; z-index:3000;
  }

  @media (max-width:1100px){
    .wrap{grid-template-columns: 1fr;}
    header{ justify-content:flex-start; padding-left:8px }
    .top-controls{ display:none }
  }
</style>
</head>
<body data-theme="dark">
  <div class="top-controls">
    <button id="themeToggle" class="theme-toggle" aria-label="Toggle theme">🌙 / ☀️</button>
  </div>

  <div class="wrap">
    <header>
      <div class="brand">
        <div class="logo" aria-hidden="true">
          <svg width="40" height="40" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" style="border-radius:8px">
            <defs><linearGradient id="g1" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#6d28d9"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
            <rect width="64" height="64" rx="12" fill="url(#g1)"/>
            <text x="32" y="40" text-anchor="middle" fill="white" font-family="Fira Code, monospace" font-weight="700" font-size="26">TA</text>
          </svg>
        </div>
        <div>
          <h1>Text Analyzer</h1>
        </div>
      </div>
    </header>

    <!-- LEFT: form -->
    <main class="card panel" id="leftPanel">
      <form method="post" action="/" enctype="multipart/form-data" id="analyzeForm" novalidate>
        <label for="text">Texte</label>
        <textarea id="text" name="text" placeholder="Colle ton texte ici...">{{ request.form.text or '' }}</textarea>

        <div class="file-drop" role="group" aria-labelledby="fileLabel" style="margin-top:12px">
          <div style="flex:1">
            <label id="fileLabel" style="font-weight:600;margin-bottom:6px;display:block">Importer un fichier</label>
            <div class="file-input">
              <div style="flex:1">
                <input id="file" name="file" type="file" onchange="onFileChange(event)" aria-label="Uploader un fichier">
                <div class="fake-file" id="fakeFile" onclick="document.getElementById('file').click()">
                  <div style="display:flex;align-items:center;gap:8px">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 7l4-4 4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <span id="fakeFileText">Choisir un fichier</span>
                  </div>
                  <div><button type="button" class="btn secondary" onclick="document.getElementById('file').click();return false">Parcourir</button></div>
                </div>
              </div>
            </div>
            <div class="muted" id="uploadPreview" style="margin-top:8px"></div>
          </div>
        </div>

        <div class="controls" style="margin-top:14px">
          <button id="analyzeBtn" class="btn" type="submit">Analyser</button>
          <a class="btn secondary" href="{{ url_for('use_sample') }}" style="text-decoration:none">Analyser le fichier exemple</a>
          <a class="btn secondary" href="/download/report.txt" style="text-decoration:none">Télécharger report.txt</a>
        </div>

        <!-- word cloud displayed under the controls -->
        <div id="wordCloudWrap" style="display:none;">
          <div style="font-weight:600;margin-bottom:8px;color:var(--muted)">Nuage de mots</div>
          <canvas id="wordCloud"></canvas>
          <div id="cloudActions">
            <button id="downloadCloud" class="btn secondary" type="button">Télécharger nuage (PNG)</button>
          </div>
        </div>

      </form>

      {% if error %}
        <div style="margin-top:12px" class="empty-note" id="serverError">{{ error }}</div>
      {% endif %}
    </main>

    <!-- RIGHT: results -->
    <aside class="card results" id="rightResults">
      <div class="kpi"><div class="label">Statut</div><div class="value">{{ 'Analysé' if analyzed else 'Prêt' }}</div></div>

      {% if analyzed %}
        <div class="kpi"><div class="label">Total mots</div><div class="value">{{ total_words }}</div></div>
        <div class="kpi"><div class="label">Mots uniques</div><div class="value">{{ unique_words }}</div></div>

        <hr class="sep"/>

        <div style="font-weight:600;color:var(--muted);margin-bottom:6px">Détails</div>
        <div style="margin-bottom:8px">
          <strong>Début par voyelle:</strong> {{ vowels_start }} &nbsp; — &nbsp;
          <strong>Mots ≥7 lettres:</strong> {{ ge7 }}
        </div>
        <div style="margin-bottom:8px">
          <strong>Mot le plus long:</strong> {{ longest }}<br>
          <strong>Mot le plus court:</strong> {{ shortest }}
        </div>

        <div style="margin-top:6px">
          <div style="font-weight:600;color:var(--muted);margin-bottom:6px">Top {{ top_n }} mots</div>
          <table aria-live="polite">
            <thead><tr><th>Mot</th><th>Count</th></tr></thead>
            <tbody>
              {% for w,c in top %}
              <tr><td>{{ w }}</td><td>{{ c }}</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      {% else %}
        <div class="empty-note">Les résultats s'afficheront ici après avoir cliqué sur <strong>Analyser</strong>.</div>
      {% endif %}
    </aside>

  </div>

<div class="toasts" id="toasts" aria-live="polite" aria-atomic="true"></div>
<div id="cloudTooltip"></div>

<script>
  // Theme toggle
  const themeToggle = document.getElementById('themeToggle');
  const body = document.body;
  function setTheme(t){
    body.setAttribute('data-theme', t);
    localStorage.setItem('ta-theme', t);
    themeToggle.innerText = t === 'dark' ? '🌙 / ☀️' : '🌙 / ☀️';
  }
  themeToggle.addEventListener('click', ()=> {
    const cur = body.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    setTheme(cur === 'dark' ? 'light' : 'dark');
  });
  (function(){ const pref = localStorage.getItem('ta-theme') || 'dark'; setTheme(pref); })();

  // Toasts
  function showToast(msg, type='info', ttl=3500){
    const container = document.getElementById('toasts');
    const t = document.createElement('div');
    t.className = 'toast ' + (type==='error' ? 'error' : (type==='success' ? 'success' : 'info'));
    t.innerText = msg;
    container.appendChild(t);
    setTimeout(()=>{ t.style.opacity = '0'; t.style.transform='translateX(30px)'; }, ttl-300);
    setTimeout(()=>{ try{ container.removeChild(t); }catch(e){} }, ttl);
  }

  // file preview & drag/drop
  function onFileChange(e){
    const f = e.target.files && e.target.files[0];
    const preview = document.getElementById('uploadPreview');
    const txt = document.getElementById('fakeFileText');
    if(!f){ preview.innerText=''; txt.innerText='Choisir un fichier'; return; }
    txt.innerText = f.name + ' (' + Math.round(f.size/1024) + ' KB)';
    preview.innerText = 'Type: ' + (f.type || 'inconnu') + ' — Taille: ' + Math.round(f.size/1024) + ' KB';
  }
  const fake = document.getElementById('fakeFile');
  if (fake) {
    fake.addEventListener('dragover', (e)=>{ e.preventDefault(); fake.style.opacity = 0.9; });
    fake.addEventListener('dragleave', ()=>{ fake.style.opacity = 1; });
    fake.addEventListener('drop', (e)=>{ e.preventDefault(); fake.style.opacity = 1;
      const dt = e.dataTransfer;
      if(dt && dt.files && dt.files.length) {
        document.getElementById('file').files = dt.files;
        onFileChange({ target: document.getElementById('file') });
      }
    });
  }

  // disable analyze while submitting
  const form = document.getElementById('analyzeForm');
  const analyzeBtn = document.getElementById('analyzeBtn');
  form.addEventListener('submit', function(e){
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = 'Analyse en cours…';
  });

  // server error as toast
  {% if error %}
    document.addEventListener('DOMContentLoaded', ()=> {
      const msg = {{ error|tojson }};
      if (msg) showToast(msg, 'error', 5000);
    });
  {% endif %}

  // ========== Word cloud drawing (improved contrast + tooltip + download) ==========
  window._cloudPlaced = []; // global store of placed words for hover detection
  function paletteForTheme(theme){
    if(theme === 'dark'){
      return ["#ffffff","#bfefff","#9be7ff","#9b7bff","#ffb6ff","#80ffe9"];
    } else {
      return ["#002b46","#075985","#0284c7","#7c3aed","#6d28d9","#0b3948"];
    }
  }
  function chooseColorFromPalette(t, theme){
    const pal = paletteForTheme(theme);
    const idx = Math.min(pal.length - 1, Math.floor(t * pal.length));
    return pal[idx];
  }

  function drawWordCloud(words){
    if(!words || !words.length) return;
    const wrap = document.getElementById('wordCloudWrap');
    const canvas = document.getElementById('wordCloud');
    wrap.style.display = 'block';

    const rect = wrap.getBoundingClientRect();
    const cssW = Math.max(300, rect.width);
    const cssH = 220;
    const ratio = window.devicePixelRatio || 1;

    canvas.style.width = cssW + 'px';
    canvas.style.height = cssH + 'px';
    canvas.width = Math.round(cssW * ratio);
    canvas.height = Math.round(cssH * ratio);

    const ctx = canvas.getContext('2d');
    ctx.setTransform(1,0,0,1,0,0);
    ctx.scale(ratio, ratio);
    ctx.clearRect(0,0,cssW, cssH);
    ctx.textBaseline = 'top';

    const counts = words.map(w=>w[1]);
    const minc = Math.min(...counts);
    const maxc = Math.max(...counts);
    function fontSizeFor(c){
      if(maxc === minc) return 22;
      return 14 + Math.round((c - minc)/(maxc - minc) * 44);
    }

    const placed = [];
    const W = cssW;
    const H = cssH;
    const theme = document.body.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    window._cloudPlaced = [];

    for(let i=0;i<words.length;i++){
      const w = words[i][0];
      const c = words[i][1];
      const fs = fontSizeFor(c);
      ctx.font = `${fs}px Inter, sans-serif`;
      const metrics = ctx.measureText(w);
      const ww = metrics.width;
      const hh = fs * 1.15;
      let attempts = 0;
      let x,y,ok=false;
      while(attempts < 500 && !ok){
        x = Math.random()*(W - ww - 8) + 4;
        y = Math.random()*(H - hh - 8) + 4;
        ok = true;
        for(const p of placed){
          if(!(x + ww < p.x || x > p.x + p.w || y + hh < p.y || y > p.y + p.h)){
            ok = false; break;
          }
        }
        attempts++;
      }
      if(!ok){
        x = 6 + (i%6)* (Math.max(40, Math.round(ww)));
        y = 6 + Math.floor(i/6)* (hh + 6);
      }

      const t = (c - minc) / (maxc - minc || 1);
      const color = chooseColorFromPalette(t, theme);

      // stroke for better contrast
      if(theme === 'dark'){
        ctx.lineWidth = Math.max(1, Math.round(fs/14));
        ctx.strokeStyle = 'rgba(0,0,0,0.45)';
      } else {
        ctx.lineWidth = Math.max(1, Math.round(fs/14));
        ctx.strokeStyle = 'rgba(255,255,255,0.85)';
      }
      ctx.strokeText(w, x, y);
      ctx.fillStyle = color;
      ctx.fillText(w, x, y);

      placed.push({x,y,w:ww,h:hh,word:w,count:c});
      // store scaled coordinates for hover detection (CSS coordinates, not device pixels)
      window._cloudPlaced.push({x,y,w:ww,h:hh,word:w,count:c});
    }
  }

  // hover tooltip
  const canvas = document.getElementById('wordCloud');
  const tooltip = document.getElementById('cloudTooltip');
  function showTooltip(text, clientX, clientY){
    tooltip.style.display = 'block';
    tooltip.innerText = text;
    const pad = 12;
    let left = clientX + pad;
    let top = clientY + pad;
    // avoid overflow right/bottom
    if(left + tooltip.offsetWidth > window.innerWidth - 10) left = clientX - tooltip.offsetWidth - pad;
    if(top + tooltip.offsetHeight > window.innerHeight - 10) top = clientY - tooltip.offsetHeight - pad;
    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
  }
  function hideTooltip(){ tooltip.style.display = 'none'; }

  function onCanvasMove(e){
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const list = window._cloudPlaced || [];
    for(const p of list){
      if(x >= p.x && x <= p.x + p.w && y >= p.y && y <= p.y + p.h){
        showTooltip(p.word + ' — ' + p.count, e.clientX, e.clientY);
        canvas.style.cursor = 'pointer';
        return;
      }
    }
    hideTooltip();
    canvas.style.cursor = 'default';
  }
  function onCanvasLeave(){ hideTooltip(); canvas.style.cursor = 'default'; }

  if(canvas){
    canvas.addEventListener('mousemove', onCanvasMove);
    canvas.addEventListener('mouseleave', onCanvasLeave);
  }

  // download cloud PNG
  const downloadBtn = document.getElementById('downloadCloud');
  if(downloadBtn){
    downloadBtn.addEventListener('click', function(){
      const c = document.getElementById('wordCloud');
      if(!c) return;
      const tmp = c.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = 'wordcloud.png';
      link.href = tmp;
      link.click();
    });
  }

  // If server passed top words, render the cloud on load
  document.addEventListener('DOMContentLoaded', ()=> {
    try {
      const top = {{ top|tojson }};
      if(top && top.length){
        const words = top.slice(0, 40); // up to 40 words
        drawWordCloud(words);
      } else {
        const wrap = document.getElementById('wordCloudWrap');
        if(wrap) wrap.style.display = 'none';
      }
    } catch(e){
      // ignore
    }
    const serverErr = document.getElementById('serverError');
    if(serverErr && serverErr.innerText.trim()){
      showToast(serverErr.innerText.trim(), 'error', 5000);
    }
  });

</script>
</body>
</html>
"""

# -----------------------
# Server-side text utils
# -----------------------
STOPWORDS = {
    # French minimal stopwords (extend as needed)
    "le","la","les","de","des","un","une","et","du","en","a","au","aux","ce","ces","dans","par","pour",
    "sur","est","qui","se","sont","il","elle","je","tu","nous","vous","ne","pas","mais","ou","avec",
    "ou","donc","or","ni","car","l","d","s","c"
}

def remove_accents(s: str) -> str:
    nk = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nk if not unicodedata.combining(c))

def clean_text(text: str) -> str:
    text = text.lower()
    text = remove_accents(text)
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def analyze_text(text: str):
    cleaned = clean_text(text)
    words_all = cleaned.split()
    # filter stopwords for analytics that drive the cloud/top
    words = [w for w in words_all if w and w not in STOPWORDS]
    freq = Counter(words)
    total_words = len(words_all)
    unique_words = len(set(words_all))
    top = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:50]
    longest = max(words_all, key=len) if words_all else ""
    shortest = min(words_all, key=len) if words_all else ""
    vowels_start = sum(1 for w in words_all if w and w[0] in "aeiou")
    ge7 = sum(1 for w in words_all if len(w) >= 7)
    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "top": top,
        "longest": longest,
        "shortest": shortest,
        "vowels_start": vowels_start,
        "ge7": ge7,
    }

REPORT_DIR = Path.cwd()
REPORT_FILE = REPORT_DIR / "report.txt"

def write_report(data):
    lines = []
    lines.append(f"Total words: {data['total_words']}")
    lines.append(f"Unique words: {data['unique_words']}")
    lines.append("")
    lines.append("Top words:")
    for w,c in data["top"]:
        lines.append(f"{w}: {c}")
    lines.append("")
    lines.append(f"Longest word: {data['longest']}")
    lines.append(f"Shortest word: {data['shortest']}")
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

def extract_text_from_bytes(b: bytes, filename: str):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            txt = b.decode(enc)
            if txt.strip():
                return txt, None
        except Exception:
            pass

    name = filename.lower()
    if name.endswith(".pdf"):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(b))
            pages = [ (p.extract_text() or "") for p in reader.pages ]
            text = "\n".join(pages).strip()
            return text, None if text else ("", "Aucun texte extrait du PDF.")
        except ImportError:
            return "", "Installe PyPDF2 (pip install PyPDF2) pour l'extraction de PDF."
        except Exception as e:
            return "", f"Erreur extraction PDF: {e}"

    if name.endswith(".docx"):
        try:
            import docx
            from io import BytesIO
            doc = docx.Document(BytesIO(b))
            paragraphs = [p.text for p in doc.paragraphs]
            text = "\n".join(paragraphs).strip()
            return text, None if text else ("", "Aucun texte extrait du DOCX.")
        except ImportError:
            return "", "Installe python-docx (pip install python-docx) pour extraire .docx."
        except Exception as e:
            return "", f"Erreur lecture DOCX: {e}"

    if name.endswith(".html") or name.endswith(".htm"):
        try:
            s = b.decode("utf-8", errors="ignore")
            s = re.sub(r"<(script|style).*?>.*?</\\1>", " ", s, flags=re.S|re.I)
            s = re.sub(r"<[^>]+>", " ", s)
            s = re.sub(r"\s+", " ", s).strip()
            return s, None if s else ("", "Aucun texte trouvé dans le HTML.")
        except Exception:
            pass

    return "", "Impossible de décoder automatiquement le fichier. Convertis en .txt ou installe PyPDF2 / python-docx pour PDF/DOCX."

@app.route("/", methods=["GET","POST"])
def index():
    context = {"analyzed": False, "top_n": 10, "error": None, "top": []}

    if request.method == "POST":
        uploaded = request.files.get("file")
        text_input = (request.form.get("text") or "").strip()
        text = ""

        if uploaded and uploaded.filename:
            try:
                raw = uploaded.read()
                text, err = extract_text_from_bytes(raw, uploaded.filename)
                if err and not text:
                    context["error"] = err
                    return render_template_string(TEMPLATE, **context)
            except Exception as e:
                context["error"] = f"Erreur lecture fichier: {e}"
                return render_template_string(TEMPLATE, **context)

        elif text_input:
            text = text_input
        else:
            context["error"] = "Aucun texte fourni. Colle du texte ou importe un fichier."
            return render_template_string(TEMPLATE, **context)

        result = analyze_text(text)
        write_report(result)
        context.update({
            "analyzed": True,
            "total_words": result["total_words"],
            "unique_words": result["unique_words"],
            "top": result["top"],
            "longest": result["longest"],
            "shortest": result["shortest"],
            "vowels_start": result["vowels_start"],
            "ge7": result["ge7"],
            "top_n": min(10, len(result["top"]))
        })

    return render_template_string(TEMPLATE, **context)

@app.route("/use-sample")
def use_sample():
    p = Path(SAMPLE_PATH)
    if not p.exists():
        return "Fichier exemple non trouvé.", 404
    try:
        raw = p.read_bytes()
        text, err = extract_text_from_bytes(raw, p.name)
        if err and not text:
            return f"Erreur: {err}", 500
        result = analyze_text(text)
        write_report(result)
        context = {
            "analyzed": True,
            "top_n": 10,
            "total_words": result["total_words"],
            "unique_words": result["unique_words"],
            "top": result["top"],
            "longest": result["longest"],
            "shortest": result["shortest"],
            "vowels_start": result["vowels_start"],
            "ge7": result["ge7"],
            "error": None
        }
        return render_template_string(TEMPLATE, **context)
    except Exception as e:
        return f"Erreur lors de la lecture du fichier exemple: {e}", 500

@app.route("/download/<path:filename>")
def download(filename):
    full = REPORT_DIR / filename
    if not full.exists():
        return "Fichier non trouvé.", 404
    return send_from_directory(REPORT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=7000, use_reloader=False)

