from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image


# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200, help_text="Iveskite knygos zanra")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"


class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100)
    last_name = models.CharField("Pavarde", max_length=100)
    # description = models.TextField('Aprašymas', max_length=2000, default='')
    description = HTMLField('Aprašymas')
    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"
        ordering = ['-id']

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
    summary = models.TextField("Aprašymas", max_length=1000, help_text="Trumpas knygos aprašymas")
    isbn = models.CharField("ISBN", max_length=13,
                            help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True, related_name='books')
    genre = models.ManyToManyField("Genre", help_text='Pasirinkite knygos zanra')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"
        ordering = ['id']

    def __str__(self):
        return f"{self.title}, {self.author}"

    def display_genre(self):
        genres = self.genre.all()
        genre_names = list(genre.name for genre in genres)
        genres_str = ", ".join(genre_names)
        return genres_str

    display_genre.short_description = "Žanras"


class BookInstance(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus UUID knygos kopijai')
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name='instances')
    due_back = models.DateField("Bus prieinama", blank=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojami'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),

    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Statusas')

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f"{self.book}, {self.uuid}"

    class Meta:
        verbose_name = "Knygos egzempliorius"
        verbose_name_plural = "Knygos egzemplioriai"
        ordering = ['-due_back']

class BookReview(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((200, 200))
            img.save(self.nuotrauka.path)
