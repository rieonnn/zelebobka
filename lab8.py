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
@login_required  # ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
def article_list():
    # ПОЛУЧАЕМ СТАТЬИ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required  # ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/create.html',
                               error='Заголовок и текст статьи не могут быть пустыми')

    # СОЗДАЕМ НОВУЮ СТАТЬЮ
    new_article = articles(
        login_id=current_user.id,  # текущий пользователь
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=False,
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
@login_required  # ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
def edit_article(article_id):
    # НАХОДИМ СТАТЬЮ
    article = articles.query.get(article_id)

    if not article:
        return "Статья не найдена", 404

    # ПРОВЕРЯЕМ, ЧТО СТАТЬЯ ПРИНАДЛЕЖИТ ТЕКУЩЕМУ ПОЛЬЗОВАТЕЛЮ
    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/edit_article.html',
                               article=article,
                               error='Заголовок и текст статьи не могут быть пустыми')

    # ОБНОВЛЯЕМ СТАТЬЮ
    article.title = title
    article.article_text = article_text

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
