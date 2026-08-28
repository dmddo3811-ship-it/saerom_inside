from flask import Flask, render_template_string, request, redirect
import os
import psycopg2 # PostgreSQL 연동 라이브러리

app = Flask(__name__)

# Render 환경변수에서 DB 접속 주소를 가져옴
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# DB 테이블 초기화
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts ORDER BY id DESC;')
    posts = cur.fetchall()
    cur.close()
    conn.close()

    html = '''
    <h1>게시판</h1>
    <form action="/add" method="POST">
        <input type="text" name="title" placeholder="제목" required><br>
        <textarea name="content" placeholder="내용" required></textarea><br>
        <button type="submit">작성하기</button>
    </form>
    <hr>
    {% for post in posts %}
        <h3>{{ post[1] }}</h3>
        <p>{{ post[2] }}</p>
        <hr>
    {% endfor %}
    '''
    return render_template_string(html, posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO posts (title, content) VALUES (%s, %s);', (title, content))
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
