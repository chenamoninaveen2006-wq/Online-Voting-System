import json
import os
import sqlite3
from flask import Flask, jsonify, request, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'voting_demo.sqlite3'))
app = Flask(__name__)


def connect():
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with connect() as con:
        con.execute('CREATE TABLE IF NOT EXISTS demo_state (key TEXT PRIMARY KEY, value_json TEXT NOT NULL)')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/api/demo-state/<key>')
def get_state(key):
    # Local student-demo persistence only. This is not an election-grade backend.
    with connect() as con:
        row = con.execute('SELECT value_json FROM demo_state WHERE key=?', (key,)).fetchone()
    if not row:
        return jsonify({'ok': True, 'exists': False})
    try:
        value = json.loads(row['value_json'])
    except json.JSONDecodeError:
        return jsonify({'ok': True, 'exists': False})
    return jsonify({'ok': True, 'exists': True, 'value': value})


@app.post('/api/demo-state/<key>')
def set_state(key):
    if len(key) > 80:
        return jsonify({'ok': False, 'error': 'State key too long.'}), 400
    data = request.get_json(silent=True) or {}
    try:
        encoded = json.dumps(data.get('value'), ensure_ascii=False, separators=(',', ':'))
    except (TypeError, ValueError):
        return jsonify({'ok': False, 'error': 'Invalid JSON value.'}), 400
    with connect() as con:
        con.execute('INSERT INTO demo_state(key,value_json) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json', (key, encoded))
    return jsonify({'ok': True})


@app.get('/health')
def health():
    return jsonify({'ok': True, 'storage': 'SQLite'})


if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '5000')), debug=False)
