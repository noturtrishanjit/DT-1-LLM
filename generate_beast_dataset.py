"""Generate a broad, license-free synthetic DT lll curriculum.

This is pattern-training data, not a replacement for a large human-authored corpus.
It deliberately covers the model's target skills without copying third-party text.
"""
import json, random
from pathlib import Path
random.seed(20261003)
TRAIN=Path('data/beast_curriculum_train.jsonl'); EVAL=Path('data/beast_curriculum_eval.jsonl')
rows=[]
def add(kind,prompt,response): rows.append({'kind':kind,'prompt':prompt,'response':response})
# Arithmetic: exact operations, percentages, fractions, order of operations.
for _ in range(3200):
    a=random.randint(-99,199); b=random.randint(-99,199); op=random.choice(['+','-','×'])
    ans=a+b if op=='+' else a-b if op=='-' else a*b
    add('math',f'Calculate {a} {op} {b} and show the steps.',f'Start with {a} {op} {b}. Compute the operation: {a} {op} {b} = {ans}. The answer is {ans}.')
for _ in range(700):
    divisor=random.randint(2,20); quotient=random.randint(2,50); dividend=divisor*quotient
    add('math',f'Divide {dividend} by {divisor} and explain the result.',f'Division asks how many groups of {divisor} fit into {dividend}. Since {divisor} × {quotient} = {dividend}, {dividend} ÷ {divisor} = {quotient}.')
for _ in range(500):
    base=random.choice([20,40,50,60,80,100,120,200,500]); pct=random.choice([5,10,15,20,25,30,40,50])
    ans=base*pct//100
    add('math',f'What is {pct} percent of {base}? Show the calculation.',f'Convert the percent to a decimal: {pct}% = {pct/100:g}. Multiply: {pct/100:g} × {base} = {ans}. The answer is {ans}.')
for _ in range(400):
    den=random.randint(2,12); n1=random.randint(1,den-1); n2=random.randint(1,den-1); total=n1+n2
    add('math',f'Add {n1}/{den} and {n2}/{den}.',f'The denominators match, so add the numerators: {n1} + {n2} = {total}. The result is {total}/{den}. Simplify it if possible.')
# Algebra: linear equations with positive and negative constants.
for _ in range(3200):
    a=random.randint(2,12); x=random.randint(-15,25); b=random.randint(-30,30); c=a*x+b
    sign='+' if b>=0 else '-'; mag=abs(b)
    add('math',f'Solve {a}x {sign} {mag} = {c} step by step.',f'Subtract {b} from both sides: {a}x = {a*x}. Divide both sides by {a}: x = {x}. Check: {a}({x}) {sign} {mag} = {c}. The answer is x = {x}.')
for _ in range(900):
    a=random.randint(2,9); b=random.randint(1,12); x=random.randint(-10,20); c=a*(x+b)
    add('math',f'Solve {a}(x + {b}) = {c}.',f'Divide both sides by {a}: x + {b} = {x+b}. Subtract {b}: x = {x}. Check: {a}({x} + {b}) = {c}.')
# Word problems with exact arithmetic.
for _ in range(1500):
    n=random.randint(2,30); each=random.randint(2,40); total=n*each
    noun=random.choice(['pencils','books','apples','stickers','coins','marbles'])
    add('math',f'There are {n} boxes with {each} {noun} in each box. How many {noun} are there?',f'Multiply boxes by items per box: {n} × {each} = {total}. There are {total} {noun}.')
for _ in range(500):
    start=random.randint(10,100); added=random.randint(2,40); spent=random.randint(1,added); end=start+added-spent
    add('math',f'A student has {start} points, earns {added}, then spends {spent}. How many points remain?',f'First add the earned points: {start} + {added} = {start+added}. Then subtract the spent points: {start+added} - {spent} = {end}. The student has {end} points.')
# Java loops and conditions.
for n in range(1,101):
    add('java',f'Write a complete Java program that prints the numbers from 1 to {n}.',f'''```java
public class Main {{
    public static void main(String[] args) {{
        for (int i = 1; i <= {n}; i++) {{
            System.out.println(i);
        }}
    }}
}}
```
The loop starts at 1 and stops after printing {n}.''')
for _ in range(900):
    n=random.randint(2,100); word='even' if n%2==0 else 'odd'
    add('java',f'Write Java code that checks whether {n} is even or odd.',f'''```java
int number = {n};
if (number % 2 == 0) {{
    System.out.println("even");
}} else {{
    System.out.println("odd");
}}
```
The remainder operator `%` checks whether division by 2 leaves a remainder.''')
for _ in range(700):
    limit=random.randint(3,30); total=limit*(limit+1)//2
    add('java',f'Write Java code to calculate the sum from 1 to {limit}.',f'''```java
int sum = 0;
for (int i = 1; i <= {limit}; i++) {{
    sum += i;
}}
System.out.println(sum); // {total}
```
Each loop adds the next number to `sum`.''')
for _ in range(500):
    a=random.randint(1,30); b=random.randint(1,30); bigger=max(a,b)
    add('java',f'Write a Java method that returns the larger of {a} and {b}.',f'''```java
static int larger(int a, int b) {{
    if (a > b) {{
        return a;
    }}
    return b;
}}

System.out.println(larger({a}, {b})); // {bigger}
```
The method compares the two values and returns the larger one.''')
for _ in range(500):
    n=random.randint(3,8); values=', '.join(str(random.randint(1,20)) for _ in range(n))
    add('java',f'Write Java code that creates an integer array with these values: {values}.',f'''```java
int[] numbers = {{{values}}};
for (int number : numbers) {{
    System.out.println(number);
}}
```
The enhanced `for` loop visits each array element.''')
# Debugging and explanation examples.
for _ in range(400):
    add('java','Why does a Java for loop use i++?', 'The expression `i++` increases i by one after each loop iteration. It lets the loop move from one integer to the next. A loop should also have a condition that eventually becomes false.')
for _ in range(400):
    add('java','What is the difference between == and = in Java?', '`=` assigns a value to a variable. `==` compares two values and produces true or false. For example, `x = 3` assigns 3, while `x == 3` checks whether x equals 3.')
# Conversation and study help.
chat=[
('What are you?','I am DT lll, a small CPU-first assistant for conversation, student math, and beginner Java.'),
('How should you answer math questions?','I should show the important steps, check the result, and state the final answer clearly.'),
('What should you do when unsure?','I should say that I am unsure instead of inventing facts, then suggest a way to verify the answer.'),
('How should Java code be formatted?','I should use a fenced `java` code block, prefer a small complete example, and explain the key syntax.'),
('Can you explain a hard idea simply?','Yes. I can start with a plain-language explanation, use a small example, and then add technical detail if needed.'),
('How can I debug a program?','Reproduce the problem, read the error message, inspect the smallest failing part, change one thing, and test again.'),
('What makes a good training example?','A good example has a clear prompt, a correct useful answer, and enough explanation for a learner to follow.'),
('Should I trust every answer?','No. Check important math, code, and factual claims. I am a small model and can make mistakes.'),
]
for _ in range(1800):
    p,r=random.choice(chat); add('chat',p,r)
random.shuffle(rows)
TRAIN.parent.mkdir(exist_ok=True)
with TRAIN.open('w',encoding='utf-8') as f:
    for row in rows: f.write(json.dumps(row,ensure_ascii=False)+'\n')
# Held-out prompts use values not directly used by most templates.
eval_rows=[
 {'kind':'math','prompt':'Solve 11x + 22 = 99 step by step.','answer':'x = 7'},
 {'kind':'math','prompt':'What is 15 percent of 240? Show the calculation.','answer':'36'},
 {'kind':'math','prompt':'There are 13 boxes with 6 books in each box. How many books are there?','answer':'78'},
 {'kind':'java','prompt':'Write a complete Java program that prints the numbers from 1 to 9.','answer':'i <= 9'},
 {'kind':'java','prompt':'Why does a Java for loop use i++?','answer':'increases i'},
 {'kind':'chat','prompt':'What should you do when unsure?','answer':'unsure'},
]
with EVAL.open('w',encoding='utf-8') as f:
    for row in eval_rows: f.write(json.dumps(row,ensure_ascii=False)+'\n')
print(f'generated {len(rows)} training records and {len(eval_rows)} evaluation records')
