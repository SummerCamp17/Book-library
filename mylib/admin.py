from django.contrib import admin


# Register your models here.
from .models import Genre,Author,Book
admin.site.register(Genre)
admin.site.register(Author)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


admin.site.register(Book,BookAdmin)