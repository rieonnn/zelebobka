from flask import Flask, url_for, request, redirect, abort, render_template
import datetime


app = Flask(__name__)

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

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>
        Flask — фреймворк для создания веб-приложений на языке программирования Python,
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
        Относится к категории так называемых микрофреймворков — минималистичных
        каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <hr>
        <a href="/">На главную</a>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/reset_counter">/lab1/reset_counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/created">/lab1/created</a></li>
            <li><a href="/cause_error">/cause_error</a></li>
            <li><a href="/error/400">/error/400</a></li>
            <li><a href="/error/401">/error/401</a></li>
            <li><a href="/error/402">/error/402</a></li>
            <li><a href="/error/403">/error/403</a></li>
            <li><a href="/error/405">/error/405</a></li>
            <li><a href="/error/418">/error/418</a></li>
        </ul>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plan; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Андреева Ирина Александровна"
    group = "ФБИ-33"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

from flask import make_response

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    html = f'''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Дуб</title>
        <link rel="stylesheet" href="{css}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{path}" alt="oak">
    </body>
</html>
'''
    response = make_response(html)
    # Стандартный заголовок языка
    response.headers['Content-Language'] = 'ru'
    # Два своих кастомных
    response.headers['X-Lab-Work'] = 'Lab1'
    response.headers['X-Author'] = 'Andreeva Irina'
    return response

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + str(url) + '''<br>
        Ваш IP-адрес: ''' + str(client_ip) + '''<br>
        <a href="/lab1/reset_counter">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик очищен!</h1>
        <a href="/lab1/counter">Вернуться к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route('/lab2/a/')
def a():
    return 'со слэшем'

@app.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''
@app.route('/lab2/example')
def example():
    name = 'Ирина Андреева'
    return render_template('example.html', name=name)
