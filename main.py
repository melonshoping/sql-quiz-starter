from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)

with open('problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/quiz/<int:q>', methods=['GET', 'POST'])
def quiz(q):
    if q > len(problems):
        return "모든 문제를 풀었습니다!"

    problem = problems[q-1]
    result = None
    message = ''
    correct = False
    submitted_sql = ''
    trial = 0

    if request.method == 'POST':
        submitted_sql = request.form['sql']
        trial = int(request.form['trial']) + 1

        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        try:
            cursor.execute(submitted_sql)
            result = cursor.fetchall()

            cursor.execute(problem['answer'])
            correct_result = cursor.fetchall()

            if result == correct_result:
                message = "정답입니다! 🎉"
                correct = True
            else:
                message = "오답입니다. 다시 시도해보세요."
        except Exception:
            result = None
            message = "쿼리 실행 에러! 다시 시도해보세요."
        conn.close()

    return render_template('quiz.html', problem=problem, q=q, result=result,
                           message=message, correct=correct, submitted_sql=submitted_sql, trial=trial)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
