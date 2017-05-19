from django.contrib import admin


# Register your models here.
from .models import Genre, Author, Book, BookInstance, IssueRequest, Notification
admin.site.register(Genre)
admin.site.register(Author)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'no_instance', 'genre')


admin.site.register(Book, BookAdmin)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status', 'borrower', 'due_back')
    list_filter = ('book', 'status', 'due_back', 'borrower')

admin.site.register(BookInstance, BookInstanceAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'return_date')
    list_filter = ('user', 'book', 'status')

admin.site.register(IssueRequest, IssueAdmin)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notice')
    list_filter = ('user','notice')

admin.site.register(Notification, NoteAdmin)


