from flask import Flask, render_template, request, redirect
import sqlite3
import json

app = Flask(__name__)

# 문제 로딩
with open('problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/quiz/<int:q>', methods=['GET', 'POST'])
def quiz(q):
    if q > len(problems):
        return redirect('/complete')

    problem = problems[q-1]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    message = ""
    result = []
    correct = False
    trial = int(request.args.get('trial', 0))

    if request.method == 'POST':
        submitted_sql = request.form['sql']
        trial = int(request.form['trial'])
        try:
            c.execute(submitted_sql)
            result = c.fetchall()
            conn.commit()
            if submitted_sql.strip().lower().replace(" ", "") == problem['answer'].strip().lower().replace(" ", ""):
                correct = True
            elif result == eval(problem['result']):
                correct = True
            else:
                message = "오답입니다. 다시 시도하세요."
                trial += 1
        except Exception as e:
            message = f"에러 발생: {str(e)}"
            trial += 1
        conn.close()
        return render_template('quiz.html', problem=problem, q=q, result=result,
                               correct=correct, submitted_sql=submitted_sql,
                               message=message, trial=trial)

    conn.close()
    return render_template('quiz.html', problem=problem, q=q, result=result,
                           correct=correct, submitted_sql="", message=message,
                           trial=trial)

@app.route('/complete')
def complete():
    return render_template('complete.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
