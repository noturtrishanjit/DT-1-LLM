"""DT lll website backed by a local llama.cpp OpenAI-compatible server.

Start llama.cpp on 127.0.0.1:8080, then run this file on port 8000.
The tiny DT lll checkpoint and training controls remain available through server.py.
"""
import json, os, urllib.request, urllib.error
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
WEBSITE = ROOT / 'website'
LLAMA_URL = os.getenv('LLAMA_URL', 'http://127.0.0.1:8080/v1/chat/completions')
SYSTEM_PROMPT = '''You are DT lll, a friendly local AI assistant.
Answer in clear, natural English. Be concise but helpful. Explain math step by step and check the result.
For beginner Java, provide a complete example in a fenced java code block and explain the important lines.
For science and Indian history, distinguish facts from uncertainty and avoid inventing details.
If you do not know something, say so plainly. Use Markdown when useful.'''
app = Flask(__name__, static_folder=str(WEBSITE), static_url_path='')

def call_llama(prompt, max_tokens=320, temperature=0.65):
    payload = {
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': max(0.05, min(float(temperature), 1.2)),
        'max_tokens': max(32, min(int(max_tokens), 768)),
        'stream': False,
    }
    req = urllib.request.Request(LLAMA_URL, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            data = json.loads(response.read().decode())
    except urllib.error.URLError as exc:
        raise RuntimeError('Could not reach llama.cpp. Start the local model server first. Details: ' + str(exc))
    choices = data.get('choices') or []
    if not choices:
        raise RuntimeError('The local model returned no choices: ' + json.dumps(data)[:500])
    message = choices[0].get('message') or {}
    return str(message.get('content', '')).strip()

@app.get('/api/health')
def health():
    try:
        call_llama('Reply with the single word READY.', max_tokens=8, temperature=0.1)
        return jsonify({'ok': True, 'backend': 'llama.cpp', 'model': 'Qwen2.5-0.5B-Instruct-Q4_K_M'})
    except Exception as exc:
        return jsonify({'ok': False, 'backend': 'llama.cpp', 'error': str(exc)}), 503

@app.post('/api/chat')
def chat():
    body = request.get_json(silent=True) or {}
    prompt = str(body.get('prompt', '')).strip()
    if not prompt:
        return jsonify({'error': 'prompt is required'}), 400
    try:
        answer = call_llama(prompt, body.get('max_new_tokens', 320), body.get('temperature', 0.65))
        return jsonify({'answer': answer, 'model': 'Qwen2.5-0.5B-Instruct-Q4_K_M', 'simulated': False, 'backend': 'llama.cpp'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 503

@app.get('/api/status')
def status():
    try:
        call_llama('Reply with the single word READY.', max_tokens=8, temperature=0.1)
        return jsonify({'running': True, 'model': 'Qwen2.5-0.5B-Instruct-Q4_K_M', 'backend': 'llama.cpp'})
    except Exception as exc:
        return jsonify({'running': False, 'model': 'Qwen2.5-0.5B-Instruct-Q4_K_M', 'error': str(exc)})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def website(path):
    target = WEBSITE / path
    if path and target.is_file():
        return send_from_directory(WEBSITE, path)
    return send_from_directory(WEBSITE, 'index.html')

if __name__ == '__main__':
    print('DT lll pretrained website: http://127.0.0.1:8000')
    print('Backend: local llama.cpp at', LLAMA_URL)
    app.run(host=os.getenv('DT_HOST', '127.0.0.1'), port=int(os.getenv('DT_PORT', '8000')), debug=False)
