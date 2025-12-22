from flask import Blueprint, render_template, request, jsonify, session

lab9 = Blueprint('lab9', __name__, template_folder='templates/lab9')

# Фиксированные координаты (чтобы не мелькали при обновлении)
BOXES = [
    {"id": 0, "x": 100, "y": 150},
    {"id": 1, "x": 250, "y": 200},
    {"id": 2, "x": 400, "y": 180},
    {"id": 3, "x": 550, "y": 220},
    {"id": 4, "x": 700, "y": 160},
    {"id": 5, "x": 180, "y": 350},
    {"id": 6, "x": 330, "y": 400},
    {"id": 7, "x": 480, "y": 370},
    {"id": 8, "x": 630, "y": 420},
    {"id": 9, "x": 300, "y": 500}
]

GIFTS = [
    "С Новым годом! Пусть каждый день будет счастливым!",
    "Желаю успехов в учёбе и карьере!",
    "Пусть исполнится всё, о чём вы мечтаете!",
    "Здоровья, любви и тепла в доме!",
    "Пусть 2025 год принесёт стабильность и рост!",
    "Много любви!",
    "Пусть рядом будут верные друзья и любимые люди!",
    "Счастья, достатка и отличного настроения!",
    "Пусть все проекты сдаются в срок и на отлично!",
    "Желаю, чтобы мечты становились реальностью!"
]

@lab9.route('/lab9/')
def index():
    if 'opened' not in session:
        session['opened'] = []
    return render_template('lab9/index.html', boxes=BOXES)

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    data = request.get_json()
    box_id = data.get('id')

    if not isinstance(box_id, int) or box_id < 0 or box_id > 9:
        return jsonify({"error": "Неверный ID коробки"}), 400

    opened = session.get('opened', [])
    if box_id in opened:
        return jsonify({"error": "Вы уже открыли этот подарок"}), 409
    if len(opened) >= 3:
        return jsonify({"error": "Можно открыть только 3 подарка"}), 403

    opened.append(box_id)
    session['opened'] = opened
    return jsonify({
        "message": GIFTS[box_id],
        "image": f"/static/lab9/gift{box_id + 1}.jpg"
    })

@lab9.route('/lab9/status')
def status():
    opened = session.get('opened', [])
    return jsonify({
        "opened": opened,
        "remaining": 10 - len(opened)
    })
