import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

# Создайте таблицу книг
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT,
             author TEXT,
             description TEXT,
             genre TEXT)''')

conn.commit()
conn.close()

#Добавление книги в бд
def add_book(title, author, description, genre):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, description, genre) VALUES (?, ?, ?, ?)",
              (title, author, description, genre))
    conn.commit()
    conn.close()

#Показ книг из бд
def show_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT title, author FROM books")
    books = c.fetchall()
    conn.close()
    return books

#Удаление книги из бд
def delete_book(title, author):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE title=? AND author=?", (title, author))
    conn.commit()
    conn.close()

#Получение жанра книги
def get_genres():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT genre FROM books")
    genres = c.fetchall()
    conn.close()
    return genres

#Функция поиска книги по жанру
def filter_genre(genre):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT title, author FROM books WHERE genre=?", (genre,))
    books = c.fetchall()  # Retrieve the results from the query
    conn.close()
    return books  # Return the retrieved books

#Поиск ключевого слово из бд
def search_book(keyword):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT title, author FROM books WHERE title LIKE ? OR author LIKE ?", (f'%{keyword}%', f'%{keyword}%'))
    books = c.fetchall()
    conn.close()
    return books

#Подробная информация о книги
def get_book_details(title):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT title, author, description, genre FROM books WHERE title=?", (title,))
    book = c.fetchone()
    conn.close()
    if book:
        book_details = {
            'title': book[0],
            'author': book[1],
            'description': book[2],
            'genre': book[3]
        }
        return book_details
    else:
        return None
#Конец#