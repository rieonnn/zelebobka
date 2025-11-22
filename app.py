from flask import Flask, request
import datetime
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)

error_log = []


@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2.<br> Список лабораторных</h1>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href="/lab2">Вторая лабораторная</a></li>
            <li><a href="/lab3">Третья лабораторная</a></li>
            <li><a href="/lab4">Четвертая лабораторная</a></li>
            <li><a href="/lab5">Пятая лабораторная</a></li>
            <li><a href="/lab6">Шестая лабораторная</a></li>
        </ul>
        <hr>
        <footer>
            <p>Андреева Ирина Александровна</p>
            <p>Группа: ФБИ-33</p>
            <p>Курс: 3</p>
            <p>2025 год</p>
        </footer>
    </body>
</html>
'''


@app.errorhandler(404)
def not_found(err):
    global error_log
    time = datetime.datetime.now()
    ip = request.remote_addr
    url = request.url

    # добавляем запись в лог
    error_log.append(f"[{time}], пользователь {ip} зашёл на адрес: {url}")

    # формируем html для журнала
    log_html = "<h3>Журнал:</h3><ul>"
    for entry in error_log:
        # выделим ссылку <i>курсивом</i>
        parts = entry.split("адрес:")
        log_html += f"<li>{parts[0]} зашёл на адрес: <i>{parts[1].strip()}</i></li>"
    log_html += "</ul>"

    return f'''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Ошибка 404 — страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #fdf6f6;
                padding: 20px 40px;
            }}
            h1 {{ color: #d9534f; }}
            p {{ font-size: 16px; }}
            a {{ color: #0275d8; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            ul {{ list-style-type: disc; }}
            li {{ margin-bottom: 8px; }}
            footer {{ margin-top: 30px; font-size: 14px; color: gray; }}
            img {{ max-width: 300px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Ой! Ошибка 404</h1>
        <p>Запрашиваемая страница <b>{url}</b> не найдена.</p>
        <img src="https://http.cat/404" alt="404">
        <br>
        <p>Ваш IP: <b>{ip}</b></p>
        <p>Дата и время: <b>{time}</b></p>
        <a href="/">Вернуться на главную</a>
        <hr>
        {log_html}
        <footer>
            <p>Сервер: Flask | Лабораторная работа</p>
        </footer>
    </body>
</html>
''', 404


# Перехватчик ошибки 500
@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Ошибка 500 — внутренняя ошибка сервера</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #b52e31; }
        </style>
    </head>
    <body>
        <h1>Ошибка 500</h1>
        <p>На сервере произошла внутренняя ошибка.<br>
        Попробуйте обновить страницу позже.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500
