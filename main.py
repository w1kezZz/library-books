import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from app import library as db


class Book:
    def __init__(self, title, author, description, genre):
        self.title = title
        self.author = author
        self.description = description
        self.genre = genre


#Основа приложения, для запуска его.
class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Библиотека книг")
        
        self.books = []
        
        self.genres = db.get_genres()

        self.create_widgets()

        self.show_all_books()


    #Функия, где создаются виджеты
    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame.pack(padx=20, pady=20)
        
        self.title_label = tk.Label(self.frame, text="Название книги:", font=("Arial Bold", 12))
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        self.title_entry = tk.Entry(self.frame)
        self.title_entry.grid(row=0, column=1)
        
        self.author_label = tk.Label(self.frame, text="Автор книги:", font=("Arial Bold", 12))
        self.author_label.grid(row=1, column=0, sticky=tk.W)
        self.author_entry = tk.Entry(self.frame)
        self.author_entry.grid(row=1, column=1)
        
        self.description_label = tk.Label(self.frame, text="Описание книги:", font=("Arial Bold", 12))
        self.description_label.grid(row=2, column=0, sticky=tk.W)
        self.description_entry = tk.Entry(self.frame)
        self.description_entry.grid(row=2, column=1)
        
        self.genre_label = tk.Label(self.frame, text="Жанр книги:", font=("Arial Bold", 12))
        self.genre_label.grid(row=3, column=0, sticky=tk.W)
        self.genre_entry = tk.Entry(self.frame)  # Allow user to enter the genre
        self.genre_entry.grid(row=3, column=1)

        self.genre_combobox = ttk.Combobox(self.frame, values=self.genres)
        self.genre_combobox.grid(row=3, column=1)
        
        self.add_button = tk.Button(self.frame, text="Добавить книгу", font=("Arial Bold", 12), bg='green', command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2)
        
        self.books_listbox = tk.Listbox(self, width=50)
        self.books_listbox.pack(padx=20, pady=15)
        
        self.delete_button = tk.Button(self, text="Удалить книгу", font=("Arial Bold", 12), command=self.delete_book)
        self.delete_button.pack(pady=10)
        
        self.genre_filter_entry = tk.Entry(self)
        self.genre_filter_entry.pack(pady=10)
        self.genre_filter_button = tk.Button(self, text="Поиск по жанру", font=("Arial Bold", 12), command=self.filter_books_by_genre)
        self.genre_filter_button.pack()
        
        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=10)
        self.search_button = tk.Button(self, text="Поиск по ключевому слову", font=("Arial Bold", 12), command=self.search_books)
        self.search_button.pack()
    
        self.books_listbox.bind("<Double-Button-1>", self.show_book_details)


    #Функция, которая показывает книги из базы данных в Listbox
    def show_all_books(self):
        # Clear the books listbox
        self.books_listbox.delete(0, tk.END)

        # Retrieve books from the database
        books = db.show_books()

        # Show the books in the listbox
        for book in books:
            title, author = book
            self.books_listbox.insert(tk.END, f"{title} - {author}")
    

    #Функция добавление книги в базу данных
    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        description = self.description_entry.get()
        genre = self.genre_entry.get() if self.genre_entry.get() else self.genre_combobox.get()

        if title == "" or author == "" or description == "" or genre == "":
            messagebox.showerror("Ошибка", "Заполните поля!")
        else:
            db.add_book(title, author, description, genre)

            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)

            self.show_all_books()
            

    # Функция показывающая подробную информацию, о выбранной книге.
    def show_book_details(self, event):
        selected_index = self.books_listbox.curselection()
        if selected_index:
            selected_book = self.books_listbox.get(selected_index)
            title = selected_book.split('-')[0].strip()
            book_details = db.get_book_details(title)
            if book_details:
                details_window = tk.Toplevel(self)
                details_window.title("Подробная информация о книге")
                details_text = "\n".join([f"Название: {book_details['title']}", f"Автор: {book_details['author']}", f"Описание: {book_details['description']}", f"Жанр: {book_details['genre']}"])
                book_details_label = tk.Label(details_window, text=details_text, font=("Arial Bold", 12))
                book_details_label.pack(padx=20, pady=20)


    #Фунция, удаление книги из базы данных и Listbox
    def delete_book(self):
        selected_indexes = self.books_listbox.curselection()

        if selected_indexes:
            selected_books = [self.books_listbox.get(index).split(' - ') for index in selected_indexes]

            result = messagebox.askquestion("Удаление книги", "Вы уверены, что хотите удалить выбранные книги?")

            if result == "yes":
                for book in selected_books:
                    title, author = book[0], book[1]
                    for i, b in enumerate(self.books):
                        if b.title == title and b.author == author:
                            self.books.pop(i)
                            break
                    for i in selected_indexes:
                        db.delete_book(title, author)
                        self.books_listbox.delete(i)
        else:
            messagebox.showerror("Ошибка", "Выберите книгу, которую хотите удалить!")


    #Фунция, поиска книги по жанру
    def filter_books_by_genre(self):
        genre = self.genre_filter_entry.get()
        
        if genre == "":
            messagebox.showerror("Ошибка", "Введите жанр книги, чтобы найти ее!")
        else:
            filtered_books = db.filter_genre(genre=genre)
            
            if filtered_books:  # Check if filtered_books is not None
                self.books_listbox.delete(0, tk.END)
                for book in filtered_books:
                    title, author = book  # Use book instead of genre
                    self.books_listbox.insert(tk.END, title + " - " + author)
            else:
                messagebox.showinfo("Информация", "Книги с указанным жанром не найдены.")
    

    #Фунция, поиска книги по ключевому слову
    def search_books(self):
        keyword = self.search_entry.get().lower()
        
        if keyword == "":
            messagebox.showerror("Ошибка", "Введите ключевое слово, чтобы найти книгу!")
        else:
            search_results = db.search_book(keyword=keyword)
            
            if search_results:  # Check if filtered_books is not None
                self.books_listbox.delete(0, tk.END)
                for book in search_results:
                    title, author = book  # Use book instead of genre
                    self.books_listbox.insert(tk.END, title + " - " + author)
            else:
                messagebox.showinfo("Информация", "Книги с указанным жанром не найдены.")


app = LibraryApp()
app.mainloop()