from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)

with open('problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

@app.route('/')
def index():
    q = int(request.args.get('q', 1))
    submitted_sql = request.args.get('submitted_sql', '')

    if q > len(problems):
        return "모든 문제를 풀었습니다!"

    problem = problems[q-1]
    return render_template('index.html', problem=problem, q=q, submitted_sql=submitted_sql)

@app.route('/submit', methods=['POST'])
def submit():
    sql = request.form['sql']
    q = int(request.form['q'])
    problem = problems[q-1]

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        result = str(e)

    conn.close()
    return render_template('index.html', problem=problem, q=q, result=result, submitted_sql=sql)

@app.route('/pass')
def pass_problem():
    q = int(request.args.get('q', 1))
    if q > len(problems):
        return "모든 문제를 풀었습니다!"
    
    problem = problems[q-1]
    # PASS 시 정답 SQL을 submitted_sql로 넘겨줌
    return redirect(url_for('index', q=q, submitted_sql=problem['answer']))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
