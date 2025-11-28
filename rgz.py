from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import string

# Создаем Blueprint для РГЗ
rgz_bp = Blueprint('rgz', __name__, url_prefix='/rgz')

# ФИО студента и группа (отображаются на каждой странице)
STUDENT_INFO = {
    'fio': 'Андреева Ирина Александровна',
    'group': 'ФБИ-33'
}

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Валидация логина и пароля
def is_valid_username_password(text):
    allowed_chars = string.ascii_letters + string.digits + "!@#$%^&*()_-+={}[]|:;<>,.?/~"
    return all(c in allowed_chars for c in text) and len(text) >= 3

# Валидация email
def is_valid_email(email):
    return '@' in email and '.' in email and len(email) > 5

@rgz_bp.before_request
def before_request():
    g.student_info = STUDENT_INFO

# Главная страница РГЗ - список всех объявлений
@rgz_bp.route('/')
def index():
    conn = get_db_connection()

    posts = conn.execute('''
        SELECT p.*, u.name as author_name, u.email as author_email
        FROM posts p
        JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC
    ''').fetchall()

    conn.close()

    is_authenticated = 'user_id' in session
    return render_template('rgz/index.html',
                         posts=posts,
                         is_authenticated=is_authenticated,
                         student_info=STUDENT_INFO)

# Регистрация
@rgz_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        name = request.form['name'].strip()
        email = request.form['email'].strip()

        # Валидация
        errors = []
        if not login or not password or not name or not email:
            errors.append('Все обязательные поля должны быть заполнены')

        if not is_valid_username_password(login):
            errors.append('Логин должен содержать только латинские буквы, цифры и знаки препинания')

        if not is_valid_username_password(password):
            errors.append('Пароль должен содержать только латинские буквы, цифры и знаки препинания')

        if len(password) < 4:
            errors.append('Пароль должен быть не менее 4 символов')

        if password != confirm_password:
            errors.append('Пароли не совпадают')

        if not is_valid_email(email):
            errors.append('Некорректный email адрес')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('rgz/register.html', student_info=STUDENT_INFO)

        # Хеширование пароля и сохранение пользователя
        password_hash = generate_password_hash(password)
        conn = get_db_connection()

        try:
            conn.execute('''
                INSERT INTO users (login, password_hash, name, email)
                VALUES (?, ?, ?, ?)
            ''', (login, password_hash, name, email))
            conn.commit()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('rgz.login'))

        except sqlite3.IntegrityError as e:
            if 'login' in str(e):
                flash('Пользователь с таким логином уже существует', 'error')
            elif 'email' in str(e):
                flash('Пользователь с таким email уже существует', 'error')
            else:
                flash('Ошибка при регистрации', 'error')

        finally:
            conn.close()

    return render_template('rgz/register.html', student_info=STUDENT_INFO)

# Вход в систему
@rgz_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE login = ?', (login,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_login'] = user['login']
            session['user_name'] = user['name']
            session['is_admin'] = bool(user['is_admin'])
            flash(f'Добро пожаловать, {user["name"]}!', 'success')
            return redirect(url_for('rgz.index'))
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('rgz/login.html', student_info=STUDENT_INFO)

# Выход из системы
@rgz_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('rgz.index'))

# Создание объявления
@rgz_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        flash('Для создания объявления необходимо войти в систему', 'error')
        return redirect(url_for('rgz.login'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        if not title or not content:
            flash('Заполните все поля', 'error')
            return render_template('rgz/create_post.html', student_info=STUDENT_INFO)

        if len(title) < 3:
            flash('Тема объявления должна быть не менее 3 символов', 'error')
            return render_template('rgz/create_post.html', student_info=STUDENT_INFO)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)',
            (title, content, session['user_id'])
        )
        conn.commit()
        conn.close()

        flash('Объявление успешно создано!', 'success')
        return redirect(url_for('rgz.index'))

    return render_template('rgz/create_post.html', student_info=STUDENT_INFO)

# Мои объявления
@rgz_bp.route('/my_posts')
def my_posts():
    if 'user_id' not in session:
        flash('Необходимо войти в систему', 'error')
        return redirect(url_for('rgz.login'))

    conn = get_db_connection()
    posts = conn.execute(
        'SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('rgz/my_posts.html', posts=posts, student_info=STUDENT_INFO)

# Редактирование объявления
@rgz_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        flash('Необходимо войти в систему', 'error')
        return redirect(url_for('rgz.login'))

    conn = get_db_connection()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?', (post_id,)
    ).fetchone()

    if not post:
        flash('Объявление не найдено', 'error')
        conn.close()
        return redirect(url_for('rgz.index'))

    # Только автор может редактировать
    if post['author_id'] != session['user_id']:
        flash('У вас нет прав для редактирования этого объявления', 'error')
        conn.close()
        return redirect(url_for('rgz.index'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        if not title or not content:
            flash('Заполните все поля', 'error')
            return render_template('rgz/edit_post.html', post=post, student_info=STUDENT_INFO)

        if len(title) < 3:
            flash('Тема объявления должна быть не менее 3 символов', 'error')
            return render_template('rgz/edit_post.html', post=post, student_info=STUDENT_INFO)

        conn.execute(
            'UPDATE posts SET title = ?, content = ? WHERE id = ?',
            (title, content, post_id)
        )
        conn.commit()
        conn.close()

        flash('Объявление успешно обновлено!', 'success')
        return redirect(url_for('rgz.my_posts'))

    conn.close()
    return render_template('rgz/edit_post.html', post=post, student_info=STUDENT_INFO)

# Удаление объявления
@rgz_bp.route('/delete/<int:post_id>')
def delete_post(post_id):
    if 'user_id' not in session:
        flash('Необходимо войти в систему', 'error')
        return redirect(url_for('rgz.login'))

    conn = get_db_connection()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?', (post_id,)
    ).fetchone()

    if not post:
        flash('Объявление не найдено', 'error')
        conn.close()
        return redirect(url_for('rgz.index'))

    # Проверка прав: только автор или администратор может удалять
    if post['author_id'] != session['user_id'] and not session.get('is_admin'):
        flash('У вас нет прав для удаления этого объявления', 'error')
        conn.close()
        return redirect(url_for('rgz.index'))

    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    flash('Объявление успешно удалено!', 'success')
    return redirect(url_for('rgz.my_posts'))

# Удаление аккаунта
@rgz_bp.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash('Необходимо войти в систему', 'error')
        return redirect(url_for('rgz.login'))

    user_id = session['user_id']

    conn = get_db_connection()

    # Удаляем все объявления пользователя
    conn.execute('DELETE FROM posts WHERE author_id = ?', (user_id,))

    # Удаляем пользователя (кроме администратора)
    if not session.get('is_admin'):
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))

    conn.commit()
    conn.close()

    session.clear()

    if session.get('is_admin'):
        flash('Администратор не может удалить свой аккаунт через интерфейс', 'error')
    else:
        flash('Ваш аккаунт и все объявления удалены', 'info')

    return redirect(url_for('rgz.index'))

# Админ-панель
@rgz_bp.route('/admin')
def admin_panel():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('rgz.index'))

    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    posts = conn.execute('''
        SELECT p.*, u.name as author_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC
    ''').fetchall()
    conn.close()

    return render_template('rgz/admin.html', users=users, posts=posts, student_info=STUDENT_INFO)

# Удаление пользователя администратором
@rgz_bp.route('/admin/delete_user/<int:user_id>')
def admin_delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('rgz.index'))

    # Нельзя удалить самого себя
    if user_id == session['user_id']:
        flash('Нельзя удалить свой собственный аккаунт', 'error')
        return redirect(url_for('rgz.admin_panel'))

    conn = get_db_connection()

    # Удаляем все объявления пользователя
    conn.execute('DELETE FROM posts WHERE author_id = ?', (user_id,))

    # Удаляем пользователя
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))

    conn.commit()
    conn.close()

    flash('Пользователь и все его объявления удалены', 'success')
    return redirect(url_for('rgz.admin_panel'))

# Удаление объявления администратором
@rgz_bp.route('/admin/delete_post/<int:post_id>')
def admin_delete_post(post_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('rgz.index'))

    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    flash('Объявление удалено администратором', 'success')
    return redirect(url_for('rgz.admin_panel'))

# Функция для создания администратора
def create_admin():
    """Создает администратора вручную"""
    conn = get_db_connection()

    # Проверяем, есть ли уже администратор
    admin = conn.execute('SELECT * FROM users WHERE login = ?', ('admin',)).fetchone()

    if not admin:
        password_hash = generate_password_hash('admin123')
        conn.execute('''
            INSERT INTO users (login, password_hash, name, email, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', password_hash, 'Администратор', 'admin@example.com', True))
        conn.commit()
        print("Администратор создан: admin / admin123")
    else:
        print("ℹАдминистратор уже существует")

    conn.close()

if __name__ == '__main__':
    create_admin()
