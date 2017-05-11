from django.db import models
from django.urls import reverse

# Create your models here.
class Genre(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    summary=models.TextField(max_length=1000,null=True)
    genre=models.ManyToManyField(Genre)
    number_available=models.IntegerField()


    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book_detail',args=[str(self.id)])
