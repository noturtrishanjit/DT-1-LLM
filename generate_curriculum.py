"""Generate a small, license-free synthetic curriculum for DT lll smoke training.
This improves task coverage, but does not replace a large human-reviewed corpus.
"""
import json, random
from pathlib import Path
random.seed(11)
rows=[]
# Friendly conversation templates.
chat=[
 ("What are you?","I’m DT lll, a tiny CPU-first assistant for conversation, student math, and simple Java."),
 ("How should I ask you a question?","Ask one clear question at a time. For math, include the full equation. For Java, describe the input and expected output."),
 ("Can you admit when you are unsure?","Yes. I will say when I am unsure instead of inventing an answer, and I will suggest how to verify it."),
 ("Explain your style.","I try to be friendly, concise, and useful. I show steps for math and comments for beginner Java."),
 ("What can you help me learn?","I can help practice everyday explanations, arithmetic and algebra, and basic Java syntax."),
]
for _ in range(80):
    prompt, response = random.choice(chat)
    rows.append({"kind":"chat","prompt":prompt,"response":response})
# Algebra with varied coefficients and integer solutions.
for _ in range(500):
 a=random.randint(2,12); x=random.randint(-9,15); b=random.randint(-20,20); c=a*x+b
 sign='+' if b>=0 else '-'; mag=abs(b)
 response=(f"Solve {a}x {sign} {mag} = {c} step by step.\n"
           f"Subtract {b} from both sides: {a}x = {a*x}.\n"
           f"Divide both sides by {a}: x = {x}.\n"
           f"Check: {a}({x}) {sign} {mag} = {c}. The answer is x = {x}.")
 rows.append({"kind":"math","prompt":f"Solve {a}x {sign} {mag} = {c} step by step.","response":response})
# Arithmetic word problems.
for _ in range(180):
 a=random.randint(2,30); b=random.randint(2,30); total=a*b
 rows.append({"kind":"math","prompt":f"There are {a} boxes with {b} pencils each. How many pencils are there? Show the calculation.","response":f"Multiply the number of boxes by the pencils in each box: {a} × {b} = {total}. There are {total} pencils."})
# Beginner Java patterns.
for n in range(1,21):
 rows.append({"kind":"java","prompt":f"Write a Java loop that prints the numbers 1 to {n}.","response":f"```java\npublic class Main {{\n    public static void main(String[] args) {{\n        for (int i = 1; i <= {n}; i++) {{\n            System.out.println(i);\n        }}\n    }}\n}}\n```\nThe loop starts at 1 and continues while i is at most {n}."})
for n in range(2,22):
 rows.append({"kind":"java","prompt":f"Write Java code to calculate the sum from 1 to {n}.","response":f"```java\nint sum = 0;\nfor (int i = 1; i <= {n}; i++) {{\n    sum += i;\n}}\nSystem.out.println(sum);\n```\nThe loop adds each number to sum."})
for n in range(2,22):
 rows.append({"kind":"java","prompt":f"Write Java code that prints the even numbers from 2 to {n*2}.","response":f"```java\nfor (int i = 2; i <= {n*2}; i += 2) {{\n    System.out.println(i);\n}}\n```\nAdding 2 each time keeps i even."})
random.shuffle(rows)
Path("data").mkdir(exist_ok=True)
with Path("data/curriculum_train.jsonl").open("w",encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
# Hold out representative, unseen prompts.
eval_rows=[
 {"kind":"math","prompt":"Solve 7x - 14 = 35 step by step.","answer":"x = 7"},
 {"kind":"math","prompt":"There are 9 boxes with 7 pencils each. How many pencils are there? Show the calculation.","answer":"63"},
 {"kind":"java","prompt":"Write a Java loop that prints the numbers 1 to 7.","answer":"i <= 7"},
 {"kind":"java","prompt":"Write Java code to calculate the sum from 1 to 9.","answer":"sum += i"},
 {"kind":"chat","prompt":"What are you?","answer":"DT lll"},
]
with Path("data/curriculum_eval.jsonl").open("w",encoding="utf-8") as f:
    for r in eval_rows: f.write(json.dumps(r)+"\n")
print(f"generated {len(rows)} training records and {len(eval_rows)} evaluation records")
