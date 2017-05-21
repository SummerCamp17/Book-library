import django_filters
from .models import Book,Author,Genre,BookInstance

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['author','genre']



