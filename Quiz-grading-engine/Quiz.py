# -----------------------------------------
# QUIZ & GRADING ENGINE - CHALLENGE 5
# -----------------------------------------

questions = [
    {"text": "What is the output of 2 ** 3?", "answer": "8"},
    {"text": "Which type is returned by input() ?", "answer": "string"},
    {"text": "What keyword starts a loop in Python? (A) loop (B) for (C) repeat", "answer": "b"},
    {"text": "What method converts text to lowercase? (A) lower() (B) down() (C) small()", "answer": "a"},
    {"text": "Which structure uses key/value pairs? (A) list (B) dict (C) tuple", "answer": "b"},
    {"text": "What is the index of the first element in a list?", "answer": "0"},
    {"text": "What keyword is used for conditions? (A) if (B) cond (C) check", "answer": "a"},
    {"text": "len('Python') returns:", "answer": "6"},
    {"text": "What operator tests equality?", "answer": "=="},
    {"text": "What loop repeats while a condition is true?", "answer": "while"},
]

print("\n=== PYTHON QUIZ ===\n")

correct = 0
wrong_details = []

for q in questions:
    print(q["text"])
    user = input("Your answer: ").strip().lower()
    correct_answer = q["answer"].lower().strip()

    if user == correct_answer:
        correct += 1
    else:
        wrong_details.append((q["text"], user, q["answer"]))

print("\n=== RESULTS ===")
total = len(questions)
score = correct / total * 100

# grading
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "Fail"

print(f"Correct: {correct} / {total}")
print(f"Score  : {score:.2f} %")
print(f"Grade  : {grade}")

# detailed feedback
print("\n=== WRONG ANSWERS ===")
if not wrong_details:
    print("Perfect! All answers correct.")
else:
    for txt, user_ans, corr_ans in wrong_details:
        print(f"Q: {txt}")
        print(f"Your answer   : {user_ans}")
        print(f"Correct answer: {corr_ans}")
        print("---")

# save results
with open("results.txt", "a", encoding="utf-8") as f:
    f.write("=== Quiz attempt ===\n")
    f.write(f"Score  : {score:.2f}%\nGrade  : {grade}\n")
    f.write(f"Correct: {correct}/{total}\n")
    f.write(f"Wrong  : {total - correct}\n\n")

print("\nResults saved to results.txt.")
