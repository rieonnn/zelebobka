from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    # Проверка: логин не должен быть пустым
    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html',
                               error='Логин не может быть пустым')

    # Проверка: пароль не должен быть пустым
    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html',
                               error='Пароль не может быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            # ВАЖНО: Перед использованием login_user убедимся, что логин в ASCII
            try:
                # Пробуем стандартный способ
                login_user(user, remember=remember)
            except UnicodeEncodeError:
                # Если ошибка, используем альтернативный подход
                # 1. Вход без remember
                login_user(user, remember=False)

                # 2. Если нужно запомнить, сохраняем в сессии
                if remember:
                    from flask import session
                    session['remembered_user_id'] = user.id
                    session.permanent = True

            return redirect('/lab8/')

    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка: имя пользователя не должно быть пустым
    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                               error='Имя пользователя не может быть пустым')

    # Проверка: пароль не должен быть пустым
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()

    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # АВТОМАТИЧЕСКИЙ ЛОГИН ПОСЛЕ РЕГИСТРАЦИИ
    login_user(new_user, remember=False)

    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
def article_list():
    search_query = request.args.get('search', '').strip()

    # Строим базовый запрос
    if current_user.is_authenticated:
        # Можем видеть свои статьи + публичные статьи других
        query = articles.query.filter(
            db.or_(
                articles.login_id == current_user.id,
                articles.is_public == True
            )
        )
    else:
        # Только публичные статьи
        query = articles.query.filter_by(is_public=True)

    # Применяем поиск если есть запрос
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                articles.title.ilike(search_pattern),
                articles.article_text.ilike(search_pattern)
            )
        )

    # Сортировка: сначала свои статьи, затем публичные, по ID (новые сверху)
    if current_user.is_authenticated:
        all_articles = query.order_by(
            db.case((articles.login_id == current_user.id, 1), else_=0).desc(),
            articles.id.desc()
        ).all()
    else:
        all_articles = query.order_by(articles.id.desc()).all()

    return render_template('lab8/articles.html',
                          articles=all_articles,
                          search_query=search_query)

@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  # Получаем значение чекбокса

    if not title or not article_text:
        return render_template('lab8/create.html',
                               error='Заголовок и текст статьи не могут быть пустыми')

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=is_public,  # Сохраняем настройку публичности
        likes=0
    )

    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/articles/<int:article_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)

    if not article:
        return "Статья не найдена", 404

    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    if not title or not article_text:
        return render_template('lab8/edit_article.html',
                               article=article,
                               error='Заголовок и текст статьи не могут быть пустыми')

    article.title = title
    article.article_text = article_text
    article.is_public = is_public  # Обновляем публичность

    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/articles/<int:article_id>/delete/', methods=['POST'])
@login_required
def delete_article(article_id):
    # НАХОДИМ СТАТЬЮ
    article = articles.query.get(article_id)

    if not article:
        return "Статья не найдена", 404

    # ПРОВЕРЯЕМ, ЧТО СТАТЬЯ ПРИНАДЛЕЖИТ ТЕКУЩЕМУ ПОЛЬЗОВАТЕЛЮ
    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    # УДАЛЯЕМ СТАТЬЮ
    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')
