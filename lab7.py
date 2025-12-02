# lab7.py (в той же папке что app.py)
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import db_films  

lab7 = Blueprint('lab7', __name__)
film_db = db_films.FilmDB()

# Инициализируем БД
film_db.init_table()

# Начальные данные фильмов
initial_films = [
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения.",
    },
    {
        "title": "The Godfather",
        "title_ru": "Крестный отец",
        "year": 1972,
        "description": "Криминальная сага, повествующая о нью-йоркской сицилийской мафиозной семье Корлеоне. Фильм охватывает период 1945-1955 годов. Глава семьи, Дон Вито Корлеоне, выдаёт замуж свою дочь. В это время со Второй мировой войны возвращается его любимый сын Майкл. Майкл, герой войны, гордость семьи, не выражает желания заняться жестоким семейным бизнесом. Дон Корлеоне ведёт дела по старым правилам, но наступают иные времена, и появляются люди, желающие изменить сложившиеся порядки. На Дона Корлеоне совершается покушение.",
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Темный рыцарь",
        "year": 2008,
        "description": "Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить улицы Готэма от преступности. Сотрудничество оказывается эффективным, но скоро они обнаружат себя посреди хаоса, развязанного восходящим криминальным гением, известным напуганным горожанам под именем Джокер.",
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса. В первой истории Винсент проводит незабываемый вечер с женой Марселласа Мией. Во второй Марселлас покупает боксёра Бутча Кулиджа, чтобы тот сдал бой. В третьей истории Винсент и Джулс по нелепой случайности попадают в неприятности.",
    },
    {
        "title": "Forrest Gump",
        "title_ru": "Форрест Гамп",
        "year": 1994,
        "description": "Сидя на автобусной остановке, Форрест Гамп — не очень умный, но добрый и открытый парень — рассказывает случайным встречным историю своей необыкновенной жизни. С самого малолетства парень страдал от заболевания ног, соседские мальчишки дразнили его, но в один прекрасный день Форрест открыл в себе невероятные способности к бегу. Подруга детства Дженни всегда его поддерживала и защищала, но вскоре дороги их разошлись.",
    },
    {
        "title": "The Sopranos",
        "title_ru": "Сопрано",
        "year": 1999,
        "description": "Мафиозный босс Северного Джерси Тони Сопрано эффективно решает проблемы «семьи». Но с собственной роднёй ситуация сложнее: дети от рук отбились, брак под угрозой, в отношениях с пожилой матерью сплошное недопонимание. После серии панических атак он решает тайно посещать психотерапевта.",
    },
]

# Мигрируем начальные данные
film_db.migrate_initial_data(initial_films)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    films = film_db.get_all_films()  # ← Теперь из БД!
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    film = film_db.get_film_by_id(id)  # ← Теперь из БД!
    if film:
        return jsonify(film)
    return jsonify({'error': 'Фильм не найден'}), 404

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    film = film_db.get_film_by_id(id)
    if not film:
        return jsonify({'error': 'Фильм не найден'}), 404

    film_db.delete_film(id)  # ← Удаляем из БД!
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = film_db.get_film_by_id(id)
    if not film:
        return jsonify({'error': 'Фильм не найден'}), 404

    film_data = request.get_json()

    # Валидация
    errors = film_db.validate_film(film_data)
    if errors:
        return jsonify(errors), 400

    # Автозаполнение оригинального названия
    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()

    if not title and title_ru:
        film_data['title'] = title_ru

    # Обновление в БД
    film_db.update_film(
        id,
        film_data['title'],
        film_data['title_ru'],
        int(film_data['year']),
        film_data['description']
    )

    # Возвращаем обновленный фильм
    updated_film = film_db.get_film_by_id(id)
    return jsonify(updated_film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()

    # Валидация
    errors = film_db.validate_film(film_data)
    if errors:
        return jsonify(errors), 400

    # Автозаполнение оригинального названия
    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()

    if not title and title_ru:
        film_data['title'] = title_ru

    # Создание в БД
    film_id = film_db.add_film(
        film_data['title'],
        film_data['title_ru'],
        int(film_data['year']),
        film_data['description']
    )

    return jsonify({"id": film_id})
