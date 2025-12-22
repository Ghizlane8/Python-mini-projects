✅ Challenge 4 — To-Do & Habit Tracker (Flask Web App)
📌 Présentation du projet

Ce projet est une application web de gestion de tâches et d’habitudes développée avec Python et Flask.
Elle permet à un utilisateur de créer, organiser, suivre et gérer ses tâches quotidiennes via une interface moderne, intuitive et accessible depuis un navigateur.

L’application est locale, simple à utiliser et professionnelle, avec persistance des données grâce aux fichiers JSON.

🎯 Objectifs du challenge

Mettre en pratique :

les listes et dictionnaires

la logique conditionnelle

la manipulation de fichiers

la création d’une API REST

Construire une application web complète (backend + frontend)

Améliorer l’ergonomie, l’accessibilité et l’expérience utilisateur

🧠 Fonctionnalités principales
📝 Gestion des tâches

Ajouter une tâche avec :

un titre

une catégorie (study, work, personal, etc.)

Marquer une tâche comme :

TO DO

COMPLETED

Réouvrir une tâche complétée

Modifier une tâche existante

Supprimer une tâche

📂 Organisation & filtres

Filtrer les tâches par :

statut (All / Completed / To Do)

catégorie

Comptage automatique :

nombre total de tâches visibles

nombre total de tâches complétées

💾 Persistance des données

Sauvegarde automatique dans :

tasks.json

categories.json

Création de backups automatiques

Import / export des tâches au format JSON

🎨 Interface utilisateur

Interface moderne avec Tailwind CSS

Titre centré et mis en valeur

Mode Dark / Light

Statut des tâches clairement visible

Notifications (toast messages)

Accessibilité clavier (Enter, Escape)

🏗️ Architecture du projet
📦 To-Do-Habit-Tracker
 ┣ 📜 todo_web_app_pro.py
 ┣ 📜 tasks.json
 ┣ 📜 categories.json
 ┣ 📂 backups/
 ┗ 📜 README.md

⚙️ Technologies utilisées

Python 3

Flask

HTML / CSS

JavaScript

Tailwind CSS (CDN)

JSON (stockage des données)

▶️ Installation et exécution
1️⃣ Prérequis

Python 3.9 ou plus

Pip installé

2️⃣ Installation de Flask
pip install flask

3️⃣ Lancer l’application
python todo_web_app_pro.py

4️⃣ Accéder à l’application

Ouvre ton navigateur et visite :

http://127.0.0.1:8000

🔌 API REST (exemples)
Méthode	Endpoint	Description
GET	/api/tasks	Récupérer toutes les tâches
POST	/api/tasks	Ajouter une tâche
PUT	/api/tasks/<title>	Modifier une tâche
POST	/api/tasks/mark	Marquer une tâche
DELETE	/api/tasks/<title>	Supprimer une tâche
GET	/api/export	Exporter les tâches
POST	/api/import	Importer des tâches