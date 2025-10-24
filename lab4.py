from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    # Проверка, что второе число не равно нулю
    if x2 == 0:
        return render_template('lab4/div.html', error='Делить на ноль нельзя!')

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Если поле пустое, считаем как 0
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Если поле пустое, считаем как 1
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1

    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods = ['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    # Проверка, что оба числа не равны нулю
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut':
        # Проверка, чтобы счетчик не ушел в отрицательную область
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        # Максимальное количество деревьев - 10
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Андреев', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Строитель', 'gender': 'мужской'},
    {'login': 'arina', 'password': '111', 'name': 'Арина Нейверт', 'gender': 'женский'},
    {'login': 'vika', 'password': '555','name': 'Виктория Фот', 'gender': 'женский'},
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            # Находим имя пользователя по логину
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
        else:
            authorized = False
            login = ''
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name)

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые значения
    error = None
    if not login:
        error = 'Не введён логин'
    elif not password:
        error = 'Не введён пароль'

    if error:
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    # Проверка логина и пароля
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge')
def fridge_form():
    return render_template('lab4/fridge.html')

@lab4.route('/lab4/fridge', methods=['POST'])
def fridge():
    temperature = request.form.get('temperature')

    # Проверка на пустое значение
    if not temperature:
        error = 'Ошибка: не задана температура'
        return render_template('lab4/fridge.html', error=error)

    try:
        temperature = int(temperature)
    except ValueError:
        error = 'Ошибка: температура должна быть числом'
        return render_template('lab4/fridge.html', error=error)

    # Проверка диапазонов температуры
    if temperature < -12:
        error = 'Не удалось установить температуру — слишком низкое значение'
        return render_template('lab4/fridge.html', error=error)

    if temperature > -1:
        error = 'Не удалось установить температуру — слишком высокое значение'
        return render_template('lab4/fridge.html', error=error)

    # Определение количества снежинок
    snowflakes = 0
    if -12 <= temperature <= -9:
        snowflakes = 3
    elif -8 <= temperature <= -5:
        snowflakes = 2
    elif -4 <= temperature <= -1:
        snowflakes = 1

    return render_template('lab4/fridge.html',
                         temperature=temperature,
                         snowflakes=snowflakes,
                         success=f'Установлена температура: {temperature}°C')

@lab4.route('/lab4/grain')
def grain_form():
    return render_template('lab4/grain.html')

@lab4.route('/lab4/grain', methods=['POST'])
def grain():
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')

    # Проверка на пустые значения
    if not grain_type:
        error = 'Ошибка: не выбран тип зерна'
        return render_template('lab4/grain.html', error=error)

    if not weight:
        error = 'Ошибка: не указан вес'
        return render_template('lab4/grain.html', error=error)

    try:
        weight = float(weight)
    except ValueError:
        error = 'Ошибка: вес должен быть числом'
        return render_template('lab4/grain.html', error=error)

    # Проверка веса
    if weight <= 0:
        error = 'Ошибка: вес должен быть больше 0'
        return render_template('lab4/grain.html', error=error)

    if weight > 100:
        error = 'Извините, такого объёма сейчас нет в наличии'
        return render_template('lab4/grain.html', error=error)

    # Цены на зерно
    prices = {
        'barley': 12000,   # ячмень
        'oats': 8500,      # овёс
        'wheat': 9000,     # пшеница
        'rye': 15000       # рожь
    }

    # Названия зерна для вывода
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }

    price_per_ton = prices[grain_type]
    total_cost = weight * price_per_ton
    discount = 0
    discount_applied = False

    # Применение скидки за большой объем
    if weight > 10:
        discount = total_cost * 0.1
        total_cost -= discount
        discount_applied = True

    grain_name = grain_names[grain_type]

    return render_template('lab4/grain.html',
                         success=True,
                         grain_name=grain_name,
                         weight=weight,
                         total_cost=total_cost,
                         discount_applied=discount_applied,
                         discount=discount)
