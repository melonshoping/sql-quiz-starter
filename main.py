from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)

# 문제 파일 불러오기
with open('problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

@app.route('/')
def index():
    q = int(request.args.get('q', 1))
    submitted_sql = request.args.get('submitted_sql', '')
    message = request.args.get('message', '')
    trial = int(request.args.get('trial', 0))  # 시도횟수 추가

    if q > len(problems):
        return "모든 문제를 풀었습니다!"

    problem = problems[q-1]
    return render_template('index.html', problem=problem, q=q, submitted_sql=submitted_sql, message=message, trial=trial)

@app.route('/submit', methods=['POST'])
def submit():
    sql = request.form['sql']
    q = int(request.form['q'])
    trial = int(request.form['trial'])
    problem = problems[q-1]

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        # 사용자가 제출한 SQL 실행
        cursor.execute(sql)
        result = cursor.fetchall()

        # 정답 SQL 실행
        cursor.execute(problem['answer'])
        correct_result = cursor.fetchall()

        if result == correct_result:
            # 결과가 같으면 다음 문제로 이동
            return redirect(url_for('index', q=q+1, trial=0))
        else:
            # 결과가 다르면 다시 시도 + trial 1 증가
            message = "다시 시도해보세요!"
            return render_template('index.html', problem=problem, q=q, result=result, submitted_sql=sql, message=message, trial=trial+1)

    except Exception as e:
        result = str(e)
        message = "에러가 발생했습니다."

    conn.close()
    return render_template('index.html', problem=problem, q=q, result=result, submitted_sql=sql, message=message, trial=trial+1)

@app.route('/pass')
def pass_problem():
    q = int(request.args.get('q', 1))
    if q > len(problems):
        return "모든 문제를 풀었습니다!"
    
    problem = problems[q-1]
    # PASS할 때: 정답 SQL 입력창에 복사 + trial=0 초기화
    return redirect(url_for('index', q=q, submitted_sql=problem['answer'], trial=0))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
