from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. \
            Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, \
            царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до \
            конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым,\
            так и к охранникам, добиваясь их особого к себе расположения.",
    },
    {
        "title": "The Godfather",
        "title_ru": "Крестный отец",
        "year": 1972,
        "description": "Криминальная сага, повествующая о нью-йоркской сицилийской мафиозной семье Корлеоне. Фильм охватывает период 1945-1955 годов.\
            Глава семьи, Дон Вито Корлеоне, выдаёт замуж свою дочь. В это время со Второй мировой войны возвращается его любимый сын Майкл. \
            Майкл, герой войны, гордость семьи, не выражает желания заняться жестоким семейным бизнесом. Дон Корлеоне ведёт дела по старым правилам, \
            но наступают иные времена, и появляются люди, желающие изменить сложившиеся порядки. На Дона Корлеоне совершается покушение.",
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Темный рыцарь",
        "year": 2008,
        "description": "Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить улицы \
            Готэма от преступности. Сотрудничество оказывается эффективным, но скоро они обнаружат себя посреди хаоса, развязанного восходящим \
            криминальным гением, известным напуганным горожанам под именем Джокер.",
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса. \
            В первой истории Винсент проводит незабываемый вечер с женой Марселласа Мией. Во второй Марселлас покупает боксёра Бутча Кулиджа, чтобы тот сдал бой. В третьей истории \
            Винсент и Джулс по нелепой случайности попадают в неприятности.",
    },
    {
        "title": "Forrest Gump",
        "title_ru": "Форрест Гамп",
        "year": 1994,
        "description": "Сидя на автобусной остановке, Форрест Гамп — не очень умный, но добрый и открытый парень — рассказывает случайным встречным историю своей необыкновенной жизни. \
            С самого малолетства парень страдал от заболевания ног, соседские мальчишки дразнили его, но в один прекрасный день Форрест открыл в себе невероятные \
            способности к бегу. Подруга детства Дженни всегда его поддерживала и защищала, но вскоре дороги их разошлись.",
    },
    {
        "title": "The Sopranos",
        "title_ru": "Сопрано",
        "year": 1999,
        "description": "Мафиозный босс Северного Джерси Тони Сопрано эффективно решает проблемы «семьи». Но с собственной роднёй ситуация сложнее: дети от рук \
            отбились, брак под угрозой, в отношениях с пожилой матерью сплошное недопонимание. После серии панических атак он решает тайно посещать психотерапевта.",
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return films[id]
    abort(404)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    abort(404)  # проверка id и вызов 404

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()

        # Проверка 1: Русское название должно быть непустым
        if not film.get('title_ru') or str(film['title_ru']).strip() == '':
            return jsonify({'title_ru': 'Русское название обязательно'}), 400

        # Проверка 2: Оригинальное название должно быть непустым, если русское пустое
        # (но русское уже проверено выше, так что эта проверка всегда будет проходить)
        if (not film.get('title') or str(film['title']).strip() == '') and \
           (not film.get('title_ru') or str(film['title_ru']).strip() == ''):
            return jsonify({'title': 'Хотя бы одно название должно быть заполнено'}), 400

        # Проверка 3: Год должен быть от 1895 до текущего
        current_year = datetime.now().year
        try:
            year = int(film.get('year', 0))
            if year < 1895 or year > current_year:
                return jsonify({'year': f'Год должен быть от 1895 до {current_year}'}), 400
        except (ValueError, TypeError):
            return jsonify({'year': 'Некорректный год'}), 400

        # Проверка 4: Описание должно быть непустым и не более 2000 символов
        description = film.get('description', '')
        if not description or str(description).strip() == '':
            return jsonify({'description': 'Описание обязательно'}), 400
        if len(str(description).strip()) > 2000:
            return jsonify({'description': 'Описание не должно превышать 2000 символов'}), 400

        # Автозаполнение оригинального названия
        if (not film.get('title') or str(film['title']).strip() == '') and film.get('title_ru'):
            film['title'] = film['title_ru']

        films[id] = film
        return jsonify(films[id])
    abort(404)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    # Проверка 1: Русское название должно быть непустым
    if not film.get('title_ru') or str(film['title_ru']).strip() == '':
        return jsonify({'title_ru': 'Русское название обязательно'}), 400

    # Проверка 2: Оригинальное название должно быть непустым, если русское пустое
    if (not film.get('title') or str(film['title']).strip() == '') and \
       (not film.get('title_ru') or str(film['title_ru']).strip() == ''):
        return jsonify({'title': 'Хотя бы одно название должно быть заполнено'}), 400

    # Проверка 3: Год должен быть от 1895 до текущего
    current_year = datetime.now().year
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            return jsonify({'year': f'Год должен быть от 1895 до {current_year}'}), 400
    except (ValueError, TypeError):
        return jsonify({'year': 'Некорректный год'}), 400

    # Проверка 4: Описание должно быть непустым и не более 2000 символов
    description = film.get('description', '')
    if not description or str(description).strip() == '':
        return jsonify({'description': 'Описание обязательно'}), 400
    if len(str(description).strip()) > 2000:
        return jsonify({'description': 'Описание не должно превышать 2000 символов'}), 400

    # Автозаполнение оригинального названия
    if (not film.get('title') or str(film['title']).strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']

    films.append(film)
    return jsonify({"id": len(films) - 1})
