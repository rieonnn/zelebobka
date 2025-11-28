import sqlite3
import os

def init_db():
    # Удаляем старую БД если существует
    if os.path.exists('database.db'):
        print("Удаляем старую базу данных...")
        os.remove('database.db')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Таблица пользователей (только необходимые поля)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Таблица объявлений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("База данных успешно создана!")
    print("Структура:")
    print("   - Таблица 'users' (пользователи)")
    print("   - Таблица 'posts' (объявления)")

if __name__ == '__main__':
    init_db()
