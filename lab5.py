from flask import Blueprint, render_template, request
import psycopg2
lab5 = Blueprint('lab5', __name__, template_folder='templates', static_folder='static')

@lab5.route('/lab5/')
def index():
    username = 'anonymous'
    return render_template('/lab5/lab5.html', username=username)

@lab5.route('/lab5/login')
def login():
    return "Страница входа"

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = psycopg2.connect(
        host='127.0.0.1',
        database='irina_andreeva_knowledge_base',
        user='irina_andreeva_knowledge_base',
        password='zelebobka888'
    )
    cur = conn.cursor()

    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html',
                               error="Такой пользователь уже суцествует")

    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    conn.close()
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/list')
def list_articles():
    return "Список статей"

@lab5.route('/lab5/create')
def create_article():
    return "Создание статьи"
