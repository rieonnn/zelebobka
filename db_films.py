import sqlite3
from datetime import datetime

class FilmDB:
    def __init__(self, db_path='lab.db'):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Чтобы возвращать словари
        return conn

    def init_table(self):
        """Инициализация таблицы (если не существует)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def get_all_films(self):
        """Получить все фильмы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM films ORDER BY id')
        films = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return films

    def get_film_by_id(self, film_id):
        """Получить фильм по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM films WHERE id = ?', (film_id,))
        film = cursor.fetchone()
        conn.close()
        return dict(film) if film else None

    def add_film(self, title, title_ru, year, description):
        """Добавить новый фильм"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
            (title, title_ru, year, description)
        )
        film_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return film_id

    def update_film(self, film_id, title, title_ru, year, description):
        """Обновить фильм"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?',
            (title, title_ru, year, description, film_id)
        )
        conn.commit()
        conn.close()

    def delete_film(self, film_id):
        """Удалить фильм"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM films WHERE id = ?', (film_id,))
        conn.commit()
        conn.close()

    def migrate_initial_data(self, initial_films):
        """Мигрировать начальные данные из списка в БД"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Проверяем, есть ли уже данные
        cursor.execute('SELECT COUNT(*) FROM films')
        count = cursor.fetchone()[0]

        if count == 0:
            for film in initial_films:
                cursor.execute(
                    'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
                    (film['title'], film['title_ru'], film['year'], film['description'])
                )
            conn.commit()
            print(f"Мигрировано {len(initial_films)} фильмов в БД")

        conn.close()

    def validate_film(self, film_data):
        """Валидация данных фильма"""
        errors = {}

        # Проверка русского названия
        if not film_data.get('title_ru') or str(film_data['title_ru']).strip() == '':
            errors['title_ru'] = 'Русское название обязательно'

        # Проверка оригинального названия
        title = film_data.get('title', '')
        title_ru = film_data.get('title_ru', '')

        # Если оба названия пустые
        if not title.strip() and not title_ru.strip():
            errors['title'] = 'Хотя бы одно название должно быть заполнено'

        # Проверка года
        try:
            year = int(film_data.get('year', 0))
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Некорректный год'

        # Проверка описания
        description = film_data.get('description', '')
        if not description or str(description).strip() == '':
            errors['description'] = 'Описание обязательно'
        if len(str(description).strip()) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'

        return errors

