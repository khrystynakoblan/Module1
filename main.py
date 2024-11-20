import csv
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

class Library:
    def __init__(self, file_name):
        self.file_name = file_name
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            fieldnames = ['Назва', 'Автор', 'Рік видання', 'Жанр', 'Кількість примірників']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books)

    def add_book(self, name, author, year, genre, quantity):
        self.books.append(
            {'Назва': name, 'Автор': author, 'Рік видання': year, 'Жанр': genre, 'Кількість примірників': quantity}
        )
        self.save_books()

    def delete_book(self, name):
        self.books = [book for book in self.books if book['Назва'] != name]
        self.save_books()

    def plot_genres(self):
        genres = {}
        for book in self.books:
            genre = book['Жанр']
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1

        labels = genres.keys()
        sizes = genres.values()

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Розподіл книг за жанрами")
        plt.show()

    def plot_books_by_year(self):
        years = {}
        for book in self.books:
            year = book['Рік видання']
            if year in years:
                years[year] += 1
            else:
                years[year] = 1

        plt.bar(years.keys(), years.values())
        plt.xlabel('Рік видання')
        plt.ylabel('Кількість книг')
        plt.title("Кількість книг по роках")
        plt.show()

class GI:
    def __init__(self, root, library):
        self.root = root
        self.library = library
        self.root.title("Управління бібліотекою")

        self.tree = ttk.Treeview(root, columns=('Назва', 'Автор', 'Рік видання', 'Жанр', 'Кількість примірників'), show='headings')
        for col in ('Назва', 'Автор', 'Рік видання', 'Жанр', 'Кількість примірників'):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        buttons_frame = tk.Frame(root)
        buttons_frame.pack(fill=tk.X, pady=5)
        tk.Button(buttons_frame, text="Додати книгу", command=self.add_book_window).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Видалити книгу", command=self.delete_book_window).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Графік за жанрами", command=self.library.plot_genres).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Гістограма по роках", command=self.library.plot_books_by_year).pack(side=tk.LEFT, padx=5)

        self.load_table()

    def load_table(self):
        self.tree.delete(*self.tree.get_children())
        for book in self.library.books:
            self.tree.insert('', tk.END,
                             values=(book['Назва'], book['Автор'], book['Рік видання'], book['Жанр'], book['Кількість примірників']))

    def add_book_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Додати книгу")

        tk.Label(add_window, text="Назва").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Автор").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Рік видання").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Жанр").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Кількість примірників").grid(row=4, column=0, padx=5, pady=5)

        name_entry = tk.Entry(add_window)
        author_entry = tk.Entry(add_window)
        year_entry = tk.Entry(add_window)
        genre_entry = tk.Entry(add_window)
        quantity_entry = tk.Entry(add_window)

        name_entry.grid(row=0, column=1, padx=5, pady=5)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        year_entry.grid(row=2, column=1, padx=5, pady=5)
        genre_entry.grid(row=3, column=1, padx=5, pady=5)
        quantity_entry.grid(row=4, column=1, padx=5, pady=5)

        def save_book():
            try:
                name = name_entry.get()
                author = author_entry.get()
                year = int(year_entry.get())
                genre = genre_entry.get()
                quantity = int(quantity_entry.get())
                self.library.add_book(name, author, year, genre, quantity)
                self.load_table()
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Помилка", "Некоректні дані.")

        tk.Button(add_window, text="Зберегти", command=save_book).grid(row=5, column=0, columnspan=2, pady=10)

    def delete_book_window(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Видалити книгу")

        tk.Label(delete_window, text="Введіть назву книги для видалення").pack(pady=10)

        name_entry = tk.Entry(delete_window)
        name_entry.pack(pady=5)

        def delete_book():
            name = name_entry.get()
            if name:
                self.library.delete_book(name)
                self.load_table()
                delete_window.destroy()
            else:
                messagebox.showerror("Помилка", "Введіть назву книги.")

        tk.Button(delete_window, text="Видалити", command=delete_book).pack(pady=10)

library = Library('books.csv')
root = tk.Tk()
gui = GI(root, library)
root.mainloop()