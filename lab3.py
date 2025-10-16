from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

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
