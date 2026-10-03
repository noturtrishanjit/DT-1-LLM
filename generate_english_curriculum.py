"""Generate license-free English communication practice data for DT lll.
A dictionary is not enough for conversation, so this focuses on words in context,
grammar, dialogue, explanations, politeness, and clarification.
"""
import json, random
from pathlib import Path
random.seed(20261003)
rows=[]
def add(prompt,response,kind='english'): rows.append({'kind':kind,'prompt':prompt,'response':response})
# A compact common vocabulary used in definitions and examples.
words='''accept achieve advice afraid agree allow answer appear arrive ask avoid beautiful begin believe borrow brave build calm carry change choose clean clear clever close common compare complete correct create curious decide describe different difficult discover discuss early easy explain fair familiar famous fast careful friendly future gentle happy helpful honest important include improve kind learn listen local modern natural notice useful patient possible polite prepare question ready reason remember safe simple solve strong suggest teach thank understand useful'''.split()
for w in words:
    add(f'What does the word {w} mean?',f'{w.capitalize()} means a common idea or action related to everyday communication. Use it in a sentence that makes its meaning clear.', 'vocabulary')
    add(f'Use the word {w} in a natural sentence.',f'Here is a natural example: "The student tried to {w} the problem carefully."', 'vocabulary')
# Grammar and editing patterns.
grammar=[
 ('Correct this sentence: i am learning english.','Corrected sentence: "I am learning English." The pronoun I is capitalized, and English is a proper language name.'),
 ('Correct this sentence: she go to school every day.','Corrected sentence: "She goes to school every day." Use goes because the subject she takes the third-person singular verb form.'),
 ('What is the difference between their, there, and they are?','Their shows possession, there points to a place or idea, and they are means they’re. Example: Their books are over there because they are studying.'),
 ('How do I ask for clarification politely?','You can say: "Could you explain that another way, please?" or "I understand the first part, but could you clarify the last step?"'),
 ('How do I disagree politely?','Start with respect: "I see your point, but I understand it differently because…" Then give a short reason instead of attacking the person.'),
 ('What is a noun?','A noun names a person, place, thing, or idea. Examples include student, city, book, and honesty.'),
 ('What is a verb?','A verb describes an action or state. Examples include learn, write, think, and be.'),
 ('What is an adjective?','An adjective describes a noun. In "a clear answer," clear describes answer.'),
 ('What is the difference between can and could?','Can often describes ability or a direct possibility. Could can describe a past ability or make a request sound more polite.'),
 ('How should I structure an explanation?','State the answer first, explain the key idea in order, give a small example, and finish with a short summary.'),
]
for _ in range(1800):
    p,r=random.choice(grammar); add(p,r,'grammar')
# Everyday conversational turns.
conversations=[
 ('Hello, how are you?','Hello! I am doing well and ready to help. How are you?'),
 ('I do not understand this.','That is okay. Tell me which part is confusing, and we can go through it one step at a time.'),
 ('Can you give me a shorter answer?','Yes. I will keep the main answer and remove unnecessary detail.'),
 ('I made a mistake.','Mistakes are part of learning. Let us find the exact step that went wrong and fix it.'),
 ('Can you give me an example?','Sure. I will give a small example first, then explain why it works.'),
 ('What should I do next?','First, identify the goal. Then choose the smallest next step and check the result before continuing.'),
 ('Please explain this like I am a beginner.','Of course. I will avoid unnecessary jargon, define new terms, and use a simple example.'),
 ('That answer seems wrong.','Thank you for checking it. Let us review the assumptions and calculate the result again.'),
 ('Can you help me plan my study time?','Yes. Choose one small goal, work for a focused block, take a short break, and review what you learned.'),
 ('I need help writing a message.','Tell me who the message is for and the tone you want. I can make it friendly, formal, or concise.'),
]
for _ in range(2400):
    p,r=random.choice(conversations); add(p,r,'conversation')
# Intent variations and response behavior.
for _ in range(1600):
    topic=random.choice(['a school assignment','a Java program','a math problem','a difficult email','a new idea'])
    add(f'Help me with {topic}.',f'I can help with {topic}. Please share the exact task, what you have tried, and where you are stuck. I will respond with clear steps.', 'conversation')
for _ in range(1200):
    q=random.choice(['What if you do not know the answer?','Can you check your work?','How can I ask a better question?','How should you format code?'])
    r={'What if you do not know the answer?':'I will say that I am unsure and suggest a way to verify it instead of inventing a fact.','Can you check your work?':'Yes. I can repeat the important calculation, test an example, and point out assumptions.','How can I ask a better question?':'Include the goal, the relevant details, the expected format, and what you have already tried.','How should you format code?':'Use a fenced code block with the language name, keep the example small, and explain the important lines.'}[q]
    add(q,r,'conversation')
# Simple transformations: question/answer and polite rewrites.
for _ in range(1200):
    obj=random.choice(['send the file','explain the answer','check the number','help with the project','review the code'])
    add(f'Make this polite: "{obj}".',f'A polite version is: "Could you please {obj}?" This sounds direct but respectful.', 'writing')
random.shuffle(rows)
Path('data').mkdir(exist_ok=True)
with open('data/english_communication_train.jsonl','w',encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
eval_rows=[
 {'kind':'vocabulary','prompt':'What does the word curious mean?','answer':'curious'},
 {'kind':'grammar','prompt':'Correct this sentence: he go to work every day.','answer':'goes'},
 {'kind':'conversation','prompt':'I do not understand this.','answer':'one step'},
 {'kind':'writing','prompt':'Make this polite: "check the code".','answer':'please'},
 {'kind':'conversation','prompt':'What if you do not know the answer?','answer':'unsure'},
]
with open('data/english_communication_eval.jsonl','w',encoding='utf-8') as f:
    for r in eval_rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
print(f'generated {len(rows)} English communication records and {len(eval_rows)} evaluation records')
