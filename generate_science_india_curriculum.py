"""Generate compact, license-free science and Indian-history study examples.
These are educational patterns, not a replacement for a vetted textbook or source corpus.
"""
import json, random
from pathlib import Path
random.seed(20261003)
rows=[]
def add(kind,prompt,response): rows.append({'kind':kind,'prompt':prompt,'response':response})
science=[
 ('What is photosynthesis?','Photosynthesis is the process by which green plants use light energy to make glucose from carbon dioxide and water. Oxygen is released as a by-product.'),
 ('What is gravity?','Gravity is the attractive force between masses. Near Earth, it pulls objects toward the ground and gives falling objects acceleration.'),
 ('What is an atom?','An atom is the basic unit of an element. It has a nucleus containing protons and usually neutrons, with electrons around the nucleus.'),
 ('What is the difference between mass and weight?','Mass measures the amount of matter and is usually measured in kilograms. Weight is the force of gravity on that mass and is measured in newtons.'),
 ('What is a chemical change?','A chemical change forms one or more new substances. Signs can include gas production, a permanent color change, a precipitate, or heat being released.'),
 ('What is the water cycle?','Water evaporates, condenses into clouds, falls as precipitation, and collects or flows back through the environment. The cycle repeats.'),
 ('What is DNA?','DNA is a molecule that stores genetic instructions. Sections of DNA called genes help provide instructions for traits and biological processes.'),
 ('What is an ecosystem?','An ecosystem includes living organisms and the nonliving environment interacting in an area. Energy flows through food chains while matter cycles.'),
 ('What is a force?','A force is a push or pull that can change an object’s motion or shape. Force is measured in newtons.'),
 ('What is an electric circuit?','An electric circuit is a complete path through which electric charge can flow. A source, conductors, and components are common parts.'),
 ('What is the solar system?','The solar system includes the Sun and the objects that orbit it, including planets, dwarf planets, moons, asteroids, and comets.'),
 ('Why do seasons occur?','Seasons mainly occur because Earth’s axis is tilted as Earth orbits the Sun. The tilt changes the angle and duration of sunlight in each hemisphere.'),
 ('What is a cell?','A cell is the basic structural and functional unit of life. Some organisms have one cell, while others have many specialized cells.'),
 ('What is an acid and a base?','An acid and a base are types of chemical substances with different properties. The pH scale is commonly used to describe how acidic or basic a water-based solution is.'),
 ('What is conservation of energy?','Energy cannot be created or destroyed in an isolated system, but it can be transferred or transformed from one form to another.'),
]
for _ in range(2200):
    p,r=random.choice(science); add('science',p,r)
    if random.random()<0.45: add('science',f'Explain this for a beginner: {p}',r+' Start with the main idea, then use a simple example and avoid unnecessary jargon.')
india=[
 ('What was the Indus Valley Civilization?','The Indus Valley Civilization was an ancient urban civilization known for planned cities, drainage systems, craft production, and long-distance trade. Important sites include Harappa and Mohenjo-daro.'),
 ('What was the Maurya Empire?','The Maurya Empire was a major ancient Indian empire. Chandragupta Maurya founded it, and Ashoka later became known for supporting Buddhism and public welfare after the Kalinga War.'),
 ('Why is Ashoka important in Indian history?','Ashoka was a Mauryan emperor who, after the Kalinga War, promoted dhamma, ethical conduct, welfare, and the spread of Buddhism. His inscriptions are important historical sources.'),
 ('What was the Gupta period known for?','The Gupta period is associated with developments in mathematics, astronomy, literature, art, and political history. Historians avoid treating it as uniformly peaceful or identical across all regions.'),
 ('What were the Cholas known for?','The Cholas were a powerful south Indian dynasty known for administration, temple architecture, maritime activity, and influence in parts of South and Southeast Asia.'),
 ('What was the Delhi Sultanate?','The Delhi Sultanate refers to a series of Muslim-ruled dynasties that governed large parts of northern India from the thirteenth to the early sixteenth century.'),
 ('What was the Mughal Empire?','The Mughal Empire was founded by Babur in 1526 after the First Battle of Panipat. It developed a large imperial administration and influenced architecture, art, language, and culture.'),
 ('Why is Akbar important?','Akbar expanded and consolidated the Mughal Empire and developed administrative policies that helped govern a diverse population. His court supported art, literature, and debate.'),
 ('What was the Bhakti movement?','The Bhakti movement included devotional traditions that emphasized personal devotion and varied widely by region, language, teacher, and religious practice.'),
 ('What was the Maratha Confederacy?','The Maratha power grew in western India and later became a major political force. Its history includes the leadership of Shivaji, regional administration, military expansion, and a confederate structure.'),
 ('What was the significance of the Battle of Plassey?','The Battle of Plassey in 1757 strengthened the East India Company’s political influence in Bengal. It was an important step in the expansion of British power in India.'),
 ('What was the Revolt of 1857?','The Revolt of 1857 was a major uprising against East India Company rule involving soldiers, rulers, communities, and local grievances. Its causes and regional experiences were varied.'),
 ('What was the Indian National Congress?','The Indian National Congress was founded in 1885 and became a major organization in the Indian freedom movement, though its membership, ideas, and strategies changed over time.'),
 ('What was the Non-Cooperation Movement?','The Non-Cooperation Movement, led by Mahatma Gandhi from 1920, encouraged people to withdraw cooperation from colonial institutions. It was later suspended after violence at Chauri Chaura.'),
 ('What was the Salt March?','The Salt March of 1930 was a civil-disobedience action led by Gandhi against the British salt laws. It helped draw international attention to the independence movement.'),
 ('What was the Quit India Movement?','The Quit India Movement began in 1942 with the demand that British rule end in India. It led to arrests, protests, and underground activity during the Second World War.'),
 ('When did India become independent?','India became independent on 15 August 1947. Independence occurred alongside Partition, which caused large-scale migration and serious communal violence.'),
 ('When did the Constitution of India come into effect?','The Constitution of India came into effect on 26 January 1950, and India became a republic.'),
 ('How should Indian history be studied?','Study chronology, causes, consequences, regional differences, primary sources, and competing interpretations. Avoid reducing complex periods to a single slogan.'),
]
for _ in range(2500):
    p,r=random.choice(india); add('indian_history',p,r)
    if random.random()<0.35: add('indian_history',f'Give a short student-friendly answer: {p}',r+' A good answer should distinguish established evidence from interpretation.')
random.shuffle(rows)
Path('data').mkdir(exist_ok=True)
with open('data/science_indian_history_train.jsonl','w',encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
eval_rows=[
 {'kind':'science','prompt':'What is conservation of energy?','answer':'cannot be created or destroyed'},
 {'kind':'science','prompt':'Why do seasons occur?','answer':'Earth axis tilted'},
 {'kind':'indian_history','prompt':'When did India become independent?','answer':'15 August 1947'},
 {'kind':'indian_history','prompt':'When did the Constitution of India come into effect?','answer':'26 January 1950'},
 {'kind':'indian_history','prompt':'Why is Ashoka important in Indian history?','answer':'Kalinga'},
]
with open('data/science_indian_history_eval.jsonl','w',encoding='utf-8') as f:
    for r in eval_rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
print(f'generated {len(rows)} science and Indian-history records')
