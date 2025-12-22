🧠 Challenge 2 — Text Analyzer (Flask App)
📌 Présentation

Ce projet correspond au Challenge 2 et consiste à développer une application web de traitement et d’analyse de texte avec Python et Flask.

L’application permet d’analyser rapidement un texte ou un fichier afin d’en extraire des statistiques clés, un nuage de mots interactif, et un rapport téléchargeable, le tout via une interface moderne et responsive.

🎯 Objectifs du challenge

Manipuler et nettoyer du texte en Python

Calculer des statistiques linguistiques simples

Construire une application web avec Flask

Concevoir une interface UI/UX professionnelle

Générer des visualisations (nuage de mots)

Gérer l’upload et l’analyse de fichiers

⚙️ Fonctionnalités principales

✍️ Saisie manuelle de texte

📂 Import de fichiers (.txt, .html, .pdf, .docx)

📊 Statistiques calculées :

Nombre total de mots

Nombre de mots uniques

Mots commençant par une voyelle

Mots de longueur ≥ 7

Mot le plus long et le plus court

🔝 Top 10 des mots les plus fréquents (hors stopwords)

☁️ Nuage de mots interactif :

Taille proportionnelle à la fréquence

Tooltip au survol

Téléchargement en image (PNG)

📄 Génération automatique d’un fichier report.txt

🌗 Mode sombre / clair

🎨 Interface responsive et animée

🛠️ Technologies utilisées

Python 3

Flask

HTML / CSS / JavaScript

Canvas API (nuage de mots)

PyPDF2 (PDF – optionnel)

python-docx (DOCX – optionnel)

🚀 Lancement du projet
1️⃣ Installer les dépendances
pip install flask PyPDF2 python-docx

2️⃣ Lancer l’application
python flask_text_analyzer.py

3️⃣ Accéder à l’application
http://127.0.0.1:6000

📁 Structure du projet
Challenge-2/
│
├── flask_text_analyzer.py   # Application Flask principale
├── report.txt              # Rapport généré automatiquement
├── PyChallenges.html       # Fichier exemple
└── README.md               # Documentation

🧪 Exemple d’analyse

Texte analysé :

Python est génial. Python est puissant et flexible.


Résultats :

Total mots : 7

Mots uniques : 6

Top mot : python (2)

Nuage de mots généré dynamiquement

✅ Points forts

✔ Code structuré et lisible
✔ Bonne séparation logique (UI / traitement / serveur)
✔ Interface moderne (UX/UI)
✔ Fonctionnalités avancées pour un challenge Python
✔ Prêt pour extension (API, graphiques, NLP)

🔮 Améliorations possibles

Analyse NLP avancée (lemmatisation, sentiments)

Export PDF du rapport

Authentification utilisateur

Déploiement cloud (Render / Azure / Railway)

👩‍💻 Réalisé par

Baali Ghizlane
🎓 Master Data Science & Intelligence Artificielle
📧 Contact : baali.ghizlane2@gmail.com