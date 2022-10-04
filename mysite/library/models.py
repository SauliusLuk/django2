from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200, help_text="Iveskite knygos zanras")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100)
    last_name = models.CharField("Pavarde", max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def display_books(self):
        books = self.books.all()
        book_names = list(book.title for book in books)
        books_str = ", ".join(book_names)
        return books_str


    display_books.short_description = 'Knygos'

class Book(models.Model):
    title = models.CharField("Pavadinimas", max_length=200)
    summary = models.TextField("Aprasymas", max_length=1000, help_text="Trumpas knygos aprasymas")
    isbn = models.CharField("ISBN", max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True, related_name='books')
    genre = models.ManyToManyField("Genre", help_text='Pasirinkite knygos zanra')

    def __str__(self):
        return f"{self.title}, {self.author}"

    def display_genre(self):
        genres = self.genre.all()
        genre_names = list(genre.name for genre in genres)
        genres_str = ", ".join(genre_names)
        return genres_str

    display_genre.short_description = "Žanras"


class BookInstance(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    due_back = models.DateField("Bus prieinama", blank=True)

    def __str__(self):
        return f"{self.book}, {self.uuid}"

    class Meta:
        verbose_name = "Knygos egzempliorius"
        verbose_name_plural = "Knygos egzemplioriai"

    LOAN_STATUS = (
        ('a', 'Administruojami'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),

    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Statusas')

