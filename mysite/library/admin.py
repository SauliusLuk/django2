from django.contrib import admin
from .models import (Author, Book, BookInstance, Genre)


# Register your models here.
class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    readonly_fields = ('uuid',)
    can_delete = False
    extra = 0  # isjungia placeholderius


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'display_genre')
    inlines = [BookInstanceInLine]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'book', 'due_back', 'reader')
    list_filter = ('status', 'due_back')
    search_fields = ('uuid', 'book__title', 'book__author__last_name')

    fieldsets = (
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back', 'reader')})
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Genre)
