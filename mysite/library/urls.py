from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name="books"),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name="profile"),
    path('userbooks/', views.UserBookInstanceListView.as_view(), name='userbooks'),
    path('userbooks/<int:pk>', views.UserBookInstanceDetailView.as_view(), name='userbook'),
    path('userbooks/new', views.UserBookInstanceCreateView.as_view(), name='new_instance'),
    path('userbooks/<int:pk>/update', views.UserBookInstanceUpdateView.as_view(), name="update_instance"),
    path('userbooks/<int:pk>/delete', views.UserBookInstanceDeleteView.as_view(), name='delete_instance'),
]