from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__, template_folder='templates')

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    if name is None:
        name = "аноним"

    if age is None:
        age = "неизвестно"

    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    # Получаем параметры из оригинального заказа и пересчитываем цену
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    resp = None

    if any([color, bg_color, font_size, font_style]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color, max_age=60*60*24*30)  # 30 дней
        if bg_color:
            resp.set_cookie('bg_color', bg_color, max_age=60*60*24*30)
        if font_size:
            resp.set_cookie('font_size', font_size, max_age=60*60*24*30)
        if font_style:
            resp.set_cookie('font_style', font_style, max_age=60*60*24*30)
        return resp

    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16px')
    font_style = request.cookies.get('font_style', 'Arial, sans-serif')

    resp = make_response(render_template('lab3/settings.html',
                                        color=color,
                                        bg_color=bg_color,
                                        font_size=font_size,
                                        font_style=font_style))

    # Добавляю стили в response
    style = f"""
    <style>
        body {{
            color: {color};
            background-color: {bg_color};
            font-size: {font_size};
            font-family: {font_style};
        }}
    </style>
    """
    resp.data = resp.data.decode('utf-8').replace('</head>', style + '</head>')

    return resp

@lab3.route('/lab3/settings/clear')
def clear_settings_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', max_age=0)
    resp.set_cookie('bg_color', '', max_age=0)
    resp.set_cookie('font_size', '', max_age=0)
    resp.set_cookie('font_style', '', max_age=0)
    return resp

@lab3.route('/lab3/train_ticket', methods=['GET'])
def train_ticket_form():
    return render_template('lab3/train_ticket_form.html', errors={})


@lab3.route('/lab3/train_ticket/result', methods=['POST'])
def train_ticket_result():
    fio = request.form.get('fio', '').strip()
    shelf = request.form.get('shelf')
    linen = request.form.get('linen') == 'on'
    baggage = request.form.get('baggage') == 'on'
    insurance = request.form.get('insurance') == 'on'
    age = request.form.get('age', '').strip()
    from_city = request.form.get('from_city', '').strip()
    to_city = request.form.get('to_city', '').strip()
    date = request.form.get('date', '').strip()

    errors = {}

    # Проверка на пустые поля
    if not fio:
        errors['fio'] = 'Введите ФИО'
    if not shelf:
        errors['shelf'] = 'Выберите полку'
    if not age:
        errors['age'] = 'Введите возраст'
    if not from_city:
        errors['from_city'] = 'Укажите пункт выезда'
    if not to_city:
        errors['to_city'] = 'Укажите пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату поездки'

    # Проверка возраста
    try:
        age = int(age)
        if not (1 <= age <= 120):
            errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    except ValueError:
        errors['age'] = 'Возраст должен быть числом'

    # Если есть ошибки — вернуть форму
    if errors:
        return render_template(
            'lab3/train_ticket_form.html',
            errors=errors,
            fio=fio, shelf=shelf, linen=linen, baggage=baggage,
            insurance=insurance, age=age, from_city=from_city,
            to_city=to_city, date=date
        )

    # Расчет стоимости
    price = 700 if age < 18 else 1000
    if shelf in ['нижняя', 'нижняя боковая']:
        price += 100
    if linen:
        price += 75
    if baggage:
        price += 250
    if insurance:
        price += 150

    return render_template(
        'lab3/train_ticket_result.html',
        fio=fio, shelf=shelf, linen=linen, baggage=baggage,
        insurance=insurance, age=age, from_city=from_city,
        to_city=to_city, date=date, price=price, is_child=(age < 18)
    )

# Список товаров (смартфоны)
products = [
    {"name": "iPhone 14", "price": 900, "brand": "Apple", "color": "Black"},
    {"name": "iPhone 13", "price": 700, "brand": "Apple", "color": "White"},
    {"name": "Samsung Galaxy S23", "price": 850, "brand": "Samsung", "color": "Silver"},
    {"name": "Samsung Galaxy S22", "price": 650, "brand": "Samsung", "color": "Black"},
    {"name": "Google Pixel 7", "price": 600, "brand": "Google", "color": "White"},
    {"name": "Google Pixel 6", "price": 500, "brand": "Google", "color": "Black"},
    {"name": "OnePlus 11", "price": 750, "brand": "OnePlus", "color": "Green"},
    {"name": "OnePlus 10", "price": 550, "brand": "OnePlus", "color": "Blue"},
    {"name": "Xiaomi 13", "price": 650, "brand": "Xiaomi", "color": "Black"},
    {"name": "Xiaomi 12", "price": 500, "brand": "Xiaomi", "color": "White"},
    {"name": "Huawei P60", "price": 700, "brand": "Huawei", "color": "Gold"},
    {"name": "Huawei P50", "price": 550, "brand": "Huawei", "color": "Black"},
    {"name": "Sony Xperia 1 IV", "price": 950, "brand": "Sony", "color": "Black"},
    {"name": "Sony Xperia 5 III", "price": 700, "brand": "Sony", "color": "Gray"},
    {"name": "Motorola Edge 40", "price": 500, "brand": "Motorola", "color": "Blue"},
    {"name": "Motorola Edge 30", "price": 400, "brand": "Motorola", "color": "Black"},
    {"name": "Nokia X30", "price": 350, "brand": "Nokia", "color": "White"},
    {"name": "Nokia G60", "price": 300, "brand": "Nokia", "color": "Gray"},
    {"name": "Asus Zenfone 10", "price": 650, "brand": "Asus", "color": "Black"},
    {"name": "Asus ROG Phone 6", "price": 900, "brand": "Asus", "color": "Red"},
]

@lab3.route('/lab3/products', methods=['GET'])
def products_page():
    min_price = request.args.get('min_price') or request.cookies.get('min_price')
    max_price = request.args.get('max_price') or request.cookies.get('max_price')

    filtered_products = products.copy()

    try:
        min_price_val = float(min_price) if min_price else None
    except ValueError:
        min_price_val = None
    try:
        max_price_val = float(max_price) if max_price else None
    except ValueError:
        max_price_val = None

    if min_price_val and max_price_val and min_price_val > max_price_val:
        min_price_val, max_price_val = max_price_val, min_price_val

    if min_price_val is not None:
        filtered_products = [p for p in filtered_products if p['price'] >= min_price_val]
    if max_price_val is not None:
        filtered_products = [p for p in filtered_products if p['price'] <= max_price_val]

    prices = [p['price'] for p in products]
    min_placeholder = min(prices)
    max_placeholder = max(prices)

    resp = make_response(render_template('/lab3/products.html',
                                         products=filtered_products,
                                         count=len(filtered_products),
                                         min_price=min_price_val if min_price_val is not None else '',
                                         max_price=max_price_val if max_price_val is not None else '',
                                         min_placeholder=min_placeholder,
                                         max_placeholder=max_placeholder))
    if min_price_val is not None:
        resp.set_cookie('min_price', str(min_price_val), max_age=60*60*24*30)
    if max_price_val is not None:
        resp.set_cookie('max_price', str(max_price_val), max_age=60*60*24*30)

    return resp

@lab3.route('/lab3//products/clear', methods=['GET'])
def clear_filter():
    resp = make_response(redirect('/lab3/products'))
    resp.set_cookie('min_price', '', max_age=0)
    resp.set_cookie('max_price', '', max_age=0)
    return resp
