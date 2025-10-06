from flask import Blueprint, url_for, request, redirect, abort,  render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a/')
def a():
    return 'со слэшем'

@lab2.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330}
]

# Страница отдельного цветка
@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if not (0 <= flower_id < len(flower_list)):
        abort(404)
    return render_template("flower.html",
                           idx=flower_id,
                           flower=flower_list[flower_id])

# Добавление нового цветка
@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = (request.form.get('name') or '').strip()
    price = request.form.get('price')

    if not name:
        return render_template("error.html", message="Ошибка: вы не задали имя цветка")

    try:
        price = int(price)
    except (TypeError, ValueError):
        return render_template("error.html", message="Ошибка: некорректная цена")

    flower_list.lab2end({"name": name, "price": price})
    return render_template("add_flower.html",
                           name=name,
                           price=price,
                           count=len(flower_list))

# Удаление одного цветка по номеру
@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if not (0 <= flower_id < len(flower_list)):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('all_flowers'))

# Удаление всех цветов
@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('all_flowers'))

# Список всех цветов
@lab2.route('/lab2/all_flowers/')
def all_flowers():
    return render_template("all_flowers.html",
                           flowers=flower_list,
                           count=len(flower_list))


@lab2.route('/lab2/example')
def example():
    name, lab_number, group, course = 'Ирина Андреева', 2, 'ФБИ-33', '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html',
                            name=name,
                            lab_number=lab_number,
                            group=group,
                            course=course, fruits=fruits)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

# Роут с двумя параметрами
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    results = {
        'sum': a + b,
        'difference': a - b,
        'product': a * b,
        'quotient': a / b if b != 0 else 'undefined',
        'power': a ** b
    }
    return (
        f"<h1>Расчет с параметрами</h1>"
        f"{a} + {b} = {results['sum']}<br>"
        f"{a} - {b} = {results['difference']}<br>"
        f"{a} * {b} = {results['product']}<br>"
        f"{a} / {b} = {results['quotient']}<br>"
        f"{a}^{b} = {results['power']}"
    )

# Перенаправление с /lab2/calc/ на /lab2/calc/1/1
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

# Перенаправление с /lab2/calc/<int:a> на /lab2/calc/a/1
@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

books = [
    {"title": "Оно", "author": "Стивен Кинг", "genre": "Ужасы", "pages": 1138},
    {"title": "Сияние", "author": "Стивен Кинг", "genre": "Ужасы", "pages": 447},
    {"title": "Зелёная миля", "author": "Стивен Кинг", "genre": "Драма", "pages": 400},
    {"title": "Под куполом", "author": "Стивен Кинг", "genre": "Фантастика", "pages": 1071},
    {"title": "Мизери", "author": "Стивен Кинг", "genre": "Триллер", "pages": 400},
    {"title": "Чапаев и Пустота", "author": "Виктор Пелевин", "genre": "Философский роман", "pages": 320},
    {"title": "Generation \"П\"", "author": "Виктор Пелевин", "genre": "Сатирический роман", "pages": 432},
    {"title": "Омон Ра", "author": "Виктор Пелевин", "genre": "Сатира", "pages": 192},
    {"title": "Жизнь насекомых", "author": "Виктор Пелевин", "genre": "Философская фантастика", "pages": 256},
    {"title": "Священная книга оборотня", "author": "Виктор Пелевин", "genre": "Фантастика", "pages": 384},
]

# Обработчик для списка книг
@lab2.route('/lab2/books')
def show_books():
    return render_template("books.html", books=books)

objects = [
    {"name": "Клубника", "description": "Сочная красная ягода", "image": "object1.jpg"},
    {"name": "Малина", "description": "Маленькая и ароматная", "image": "object2.jpg"},
    {"name": "Лимон", "description": "Кислый и яркий фрукт", "image": "object3.jpg"},
    {"name": "Тыква", "description": "Оранжевый овощ для супов", "image": "object4.jpg"},
    {"name": "Котёнок", "description": "Милый пушистый друг", "image": "object5.jpg"},
    {"name": "Щенок", "description": "Игривый маленький пес", "image": "object6.jpg"},
    {"name": "Стол", "description": "Деревянный обеденный стол", "image": "object7.jpg"},
    {"name": "Стул", "description": "Удобный для сидения", "image": "object8.jpg"},
    {"name": "Машина", "description": "Красный спортивный автомобиль", "image": "object9.jpg"},
    {"name": "Велосипед", "description": "Средство передвижения на двух колёсах", "image": "object10.jpg"},
    {"name": "Мяч", "description": "Игрушка для игр на улице", "image": "object11.jpg"},
    {"name": "Книга", "description": "Интересное чтение для вечера", "image": "object12.jpg"},
    {"name": "Робот", "description": "Игрушка для ребёнка", "image": "object13.jpg"},
    {"name": "Апельсин", "description": "Сочный цитрусовый фрукт", "image": "object14.jpg"},
    {"name": "Груша", "description": "Сладкий фрукт с мягкой текстурой", "image": "object15.jpg"},
    {"name": "Машина скорой помощи", "description": "Красная с белыми полосами", "image": "object16.jpg"},
    {"name": "Кресло", "description": "Комфортное для отдыха", "image": "object17.jpg"},
    {"name": "Лампа", "description": "Освещает комнату", "image": "object18.jpg"},
    {"name": "Ёжик", "description": "Милое колючее животное", "image": "object19.jpg"},
    {"name": "Кактус", "description": "Растение с колючками", "image": "object20.jpg"},
]

# список для хранения логов
error_log = []

@lab2.route('/lab2/objects')
def show_objects():
    return render_template("objects.html", objects=objects)

@lab2.route("/error/400")
def error400():
    return "<h1>400 — Bad Request (Некорректный запрос)</h1>", 400


@lab2.route("/error/401")
def error401():
    return "<h1>401 — Unauthorized (Требуется авторизация)</h1>", 401


@lab2.route("/error/402")
def error402():
    return "<h1>402 — Payment Required (Требуется оплата)</h1>", 402


@lab2.route("/error/403")
def error403():
    return "<h1>403 — Forbidden (Доступ запрещён)</h1>", 403


@lab2.route("/error/405")
def error405():
    return "<h1>405 — Method Not Allowed (Метод не разрешён)</h1>", 405


@lab2.route("/error/418")
def error418():
    return "<h1>418 — I'm a teapot (Я чайник)</h1>", 418


# Маршрут, специально вызывающий ошибку
@lab2.route("/cause_error")
def cause_error():
    return 1 / 0  # деление на ноль вызовет ошибку 500
