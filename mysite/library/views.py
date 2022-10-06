from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author
from django.views import generic



# Create your views here.
def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Laisvos knygos (tos, kurios turi statusą 'g')
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # Kiek yra autorių
    num_authors = Author.objects.all().count()

    # Perduoti informaciją į šabloną žodyno pavidale:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


def authors(request):
    context = {
        'authors': Author.objects.all()
    }
    print(authors)
    return render(request, 'authors.html', context=context)

def author(request, author_id): # author_id paimamamas is urls.py
    context = {
            'single_author': get_object_or_404(Author, pk=author_id),
    }
    return render(request, 'author.html', context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'book'