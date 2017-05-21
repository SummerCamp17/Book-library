import django_filters
from .models import Book,Author,Genre,BookInstance

class BookFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Book
        fields = ['no_instance','author__name','genre']


