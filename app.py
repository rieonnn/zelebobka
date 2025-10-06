from flask import Flask, request
import datetime
from lab1 import lab1
from lab2 import lab2


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)


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
            <li><a href="/lab2">Вторая лабораторная</a></i>
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


# список для хранения логов
error_log = []

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


@app.route("/error/400")
def error400():
    return "<h1>400 — Bad Request (Некорректный запрос)</h1>", 400


@app.route("/error/401")
def error401():
    return "<h1>401 — Unauthorized (Требуется авторизация)</h1>", 401


@app.route("/error/402")
def error402():
    return "<h1>402 — Payment Required (Требуется оплата)</h1>", 402


@app.route("/error/403")
def error403():
    return "<h1>403 — Forbidden (Доступ запрещён)</h1>", 403


@app.route("/error/405")
def error405():
    return "<h1>405 — Method Not Allowed (Метод не разрешён)</h1>", 405


@app.route("/error/418")
def error418():
    return "<h1>418 — I'm a teapot (Я чайник)</h1>", 418


# Маршрут, специально вызывающий ошибку
@app.route("/cause_error")
def cause_error():
    return 1 / 0  # деление на ноль вызовет ошибку 500


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
