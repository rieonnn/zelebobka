from flask import Blueprint, render_template

lab8 = Blueprint('lab8', __name__)

DATABASE = 'lab.db'

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/login/')
def login():
    return "Страница входа"

@lab8.route('/lab8/register')
def register():
    return "Страница регистрации"

@lab8.route('/lab8/articles')
def articles():
    return "Список статей"

@lab8.route('/lab8/create')
def create():
    return "Создание статьи"
