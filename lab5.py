from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='irina_andreeva_knowledge_base',
            user='irina_andreeva_knowledge_base',
            password='zelebobka888'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "lab.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def get_user_id():
    login = session.get('login')
    if not login:
        return None

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    db_close(conn, cur)

    return user['id'] if user else None

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    full_name = request.form.get('full_name')

    if not login or not password or not full_name:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT Login FROM users WHERE Login = %s;", (login,))
    else:
        cur.execute("SELECT Login FROM users WHERE Login = ?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (Login, password, full_name) VALUES (%s, %s, %s);",
                   (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (Login, password, full_name) VALUES (?, ?, ?);",
                   (login, password_hash, full_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.clear()
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    user_id = get_user_id()

    conn, cur = db_connect()

    if user_id:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles
                WHERE user_id = %s OR is_public = true
                ORDER BY is_favorite DESC, id DESC
            """, (user_id,))
        else:
            cur.execute("""
                SELECT * FROM articles
                WHERE user_id = ? OR is_public = 1
                ORDER BY is_favorite DESC, id DESC
            """, (user_id,))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE is_public = true ORDER BY id DESC")
        else:
            cur.execute("SELECT * FROM articles WHERE is_public = 1 ORDER BY id DESC")

    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles, login=login, user_id=user_id)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text or not title.strip() or not article_text.strip():
        return render_template('lab5/create_article.html', error='Заполните все поля')

    user_id = get_user_id()
    if not user_id:
        return redirect('/lab5/logout')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO articles (user_id, title, article_text, is_favorite, is_public)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("""
            INSERT INTO articles (user_id, title, article_text, is_favorite, is_public)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    user_id = get_user_id()
    if not user_id:
        return redirect('/lab5/logout')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text or not title.strip() or not article_text.strip():
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error='Заполните все поля')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s
            WHERE id=%s
        """, (title, article_text, is_favorite, is_public, article_id))
    else:
        cur.execute("""
            UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=?
            WHERE id=?
        """, (title, article_text, is_favorite, is_public, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    user_id = get_user_id()
    if not user_id:
        return redirect('/lab5/logout')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users_list')
def users_list():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")

    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, full_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, full_name FROM users WHERE login=?;", (login,))

        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    full_name = request.form.get('full_name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not full_name:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user={'login': login, 'full_name': ''}, error='Заполните имя')

    if password:
        if password != confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', user={'login': login, 'full_name': full_name}, error='Пароли не совпадают')

        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name=%s, password=%s WHERE login=%s;",
                       (full_name, password_hash, login))
        else:
            cur.execute("UPDATE users SET full_name=?, password=? WHERE login=?;",
                       (full_name, password_hash, login))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name=%s WHERE login=%s;", (full_name, login))
        else:
            cur.execute("UPDATE users SET full_name=? WHERE login=?;", (full_name, login))

    db_close(conn, cur)
    return redirect('/lab5/list')
