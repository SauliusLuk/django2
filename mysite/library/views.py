from django.shortcuts import render, get_object_or_404, reverse
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from . forms import BookReviewForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView



# Create your views here.

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Laisvos knygos (tos, kurios turi statusą 'g')
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # Kiek yra autorių
    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Perduoti informaciją į šabloną žodyno pavidale:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):  # author_id paimamamas is urls.py
    context = {
        'single_author': get_object_or_404(Author, pk=author_id),
    }
    return render(request, 'author.html', context=context)


def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
    context = {
        'books': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)


from django.contrib.auth.decorators import login_required

def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user) # Kvieciam UserUpdateForm, paduodam per parametrus request.POST ir nurodom request user (pasiimam atnaujintus duomenis)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid(): # tikrinam ar formos yra valid
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile') # nukreipiam i funkcija ( ne i url)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10


class BookDetailView(generic.DetailView, FormMixin):
    model = Book
    template_name = 'book.html'
    context_object_name = 'book'
    form_class = BookReviewForm

# nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)


class UserBookInstanceListView(ListView, LoginRequiredMixin):
    model = BookInstance
    template_name = 'user_books.html'
    context_object_name = 'instances'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)

class UserBookInstanceDetailView(generic.DetailView, LoginRequiredMixin):
    model = BookInstance
    template_name = 'user_book.html'
    context_object_name = 'instance'

class UserBookInstanceCreateView(generic.CreateView, LoginRequiredMixin):
        model = BookInstance
        fields = ['book', 'due_back']
        success_url = '/library/userbooks/' # Patvirtinus forma, nukreipiama i url
        template_name = 'userbook_form.html'
        # form_class = UserBookInstanceCreateForm

        def form_valid(self, form):
            form.instance.reader = self.request.user # Nustatom reader ir pasiimam aktyvu useri
            form.instance.status = 'p'
            form.save()
            return super().form_valid(form)
