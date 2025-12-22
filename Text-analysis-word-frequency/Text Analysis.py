#!/usr/bin/env python3
# text_analysis.py
# Usage: python text_analysis.py

import re
import unicodedata
from collections import Counter
from pathlib import Path

def remove_accents(s: str) -> str:
    nk = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nk if not unicodedata.combining(c))

def clean_text(text: str) -> str:
    text = text.lower()
    text = remove_accents(text)
    # keep letters, numbers and spaces
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    # collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def build_freq(words):
    return Counter(words)

def top_n(freq, n=10):
    # returns list of (word, count) sorted by count desc then word asc
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]

def longest_word(words):
    if not words: return ""
    return max(words, key=len)

def shortest_word(words):
    if not words: return ""
    return min(words, key=len)

def starts_with_vowel_count(words):
    vowels = set("aeiou")
    return sum(1 for w in words if w and w[0] in vowels)

def ge_len_count(words, length=7):
    return sum(1 for w in words if len(w) >= length)

def write_report(path, total_words, unique_words, top10, longest, shortest):
    lines = []
    lines.append(f"Total words: {total_words}")
    lines.append(f"Unique words: {unique_words}")
    lines.append("")
    lines.append("Top 10 words:")
    for w,c in top10:
        lines.append(f"{w}: {c}")
    lines.append("")
    lines.append(f"Longest word: {longest}")
    lines.append(f"Shortest word: {shortest}")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Report saved to {path}")

def load_text_from_file(path):
    try:
        p = Path(path)
        return p.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Erreur lecture fichier: {e}")
        return None

def main():
    print("=== Text Analysis & Word Frequency Explorer ===")
    choice = input("1) Entrer texte manuellement\n2) Charger depuis fichier\nChoix (1/2) : ").strip()
    if choice == "1":
        print("Saisis ton texte (termine par une ligne vide) :")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)
    else:
        default = "/mnt/data/PyChallenges.html"
        path = input(f"Chemin fichier (laisser vide pour utiliser '{default}') : ").strip() or default
        content = load_text_from_file(path)
        if content is None:
            print("Abandon. Problème de lecture du fichier.")
            return
        text = content

    cleaned = clean_text(text)
    words = cleaned.split()
    freq = build_freq(words)
    total_words = len(words)
    unique_words = len(freq)
    top10 = top_n(freq, 10)
    longest = longest_word(words)
    shortest = shortest_word(words)
    vowels_start = starts_with_vowel_count(words)
    ge7 = ge_len_count(words, 7)

    # Affichage résumé
    print("\n--- Résumé ---")
    print(f"Total mots     : {total_words}")
    print(f"Mots uniques   : {unique_words}")
    print(f"Mots qui commencent par une voyelle : {vowels_start}")
    print(f"Mots longueur >= 7 : {ge7}")
    print(f"Mot le plus long : {longest}")
    print(f"Mot le plus court: {shortest}\n")

    # Top 10 table
    print(f"{'Word':<15} {'Count':>5}")
    print("-" * 22)
    for w,c in top10:
        print(f"{w:<15} {c:>5}")

    # Save report
    report_path = "report.txt"
    write_report(report_path, total_words, unique_words, top10, longest, shortest)
    print("\nTerminé.")

if __name__ == "__main__":
    main()
1