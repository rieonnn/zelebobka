from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user

lab9 = Blueprint('lab9', __name__, template_folder='templates/lab9')

# Фиксированные координаты (чтобы не мелькали при обновлении)
BOXES = [
    {"id": 0, "x": 100, "y": 150, "requires_auth": False},
    {"id": 1, "x": 250, "y": 200, "requires_auth": True},
    {"id": 2, "x": 400, "y": 180, "requires_auth": False},
    {"id": 3, "x": 550, "y": 220, "requires_auth": True},
    {"id": 4, "x": 700, "y": 160, "requires_auth": False},
    {"id": 5, "x": 180, "y": 350, "requires_auth": True},
    {"id": 6, "x": 330, "y": 400, "requires_auth": False},
    {"id": 7, "x": 480, "y": 370, "requires_auth": True},
    {"id": 8, "x": 630, "y": 420, "requires_auth": False},
    {"id": 9, "x": 300, "y": 500, "requires_auth": True}
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

    # Проверка авторизации для специальных подарков
    box_info = next((b for b in BOXES if b["id"] == box_id), None)
    if box_info and box_info["requires_auth"]:
        if not current_user.is_authenticated:
            return jsonify({"error": "Требуется авторизация для открытия этого подарка"}), 401

    opened = session.get('opened', [])
    if box_id in opened:
        return jsonify({"error": "Вы уже открыли этот подарок"}), 409

    # Проверка лимита на открытие
    limit = 5 if current_user.is_authenticated else 3
    if len(opened) >= limit:
        return jsonify({"error": f"Можно открыть только {limit} подарков"}), 403

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
        "remaining": 10 - len(opened),
        "is_authenticated": current_user.is_authenticated
    })

@lab9.route('/lab9/reset', methods=['POST'])
@login_required
def reset_boxes():
    """Сброс всех открытых подарков (только для авторизованных)"""
    session['opened'] = []
    return jsonify({"message": "Подарки сброшены! Все коробки снова полны!"})
