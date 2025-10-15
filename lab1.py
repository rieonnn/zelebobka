from flask import Blueprint, url_for, request, redirect, make_response
import datetime
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1/")
def lab():
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


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/image')
def image():
    path = url_for("static", filename="/lab1/oak.jpg")
    css = url_for("static", filename="/lab1/lab1.css")
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

@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset_counter')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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

# Маршрут, специально вызывающий ошибку
@lab1.route("/cause_error")
def cause_error():
    return 1 / 0  # деление на ноль вызовет ошибку 500

# Перехватчик ошибки 500
@lab1.errorhandler(500)
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
