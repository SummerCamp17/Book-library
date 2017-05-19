from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from datetime import date


# Create your models here.
class Genre(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return os.path.join('pics', str(instance.id),filename)




class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    description=models.TextField(max_length=1000,null=True,blank=True)
    genre=models.ManyToManyField(Genre)
    cover = models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    no_instance=models.IntegerField(null=True,blank=True,default=0)


    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book_detail',args=[str(self.id)])
    def image_url(self):
        if self.cover and hasattr(self.cover,'url'):
            return self.cover.url
        else:
            return '/static/1.jpg'


class IssueRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    book=models.ForeignKey(Book,on_delete=models.SET_NULL,null=True,blank=True)
    return_date=models.DateField(null=True, blank=True)
    ISSUE_STATUS = (
        ('r', 'Rejected'),
        ('a', 'Accepted'),
        ('n', 'None'),
    )
    status = models.CharField(max_length=1, choices=ISSUE_STATUS,default='n',null=True,blank=True)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notice = models.CharField(max_length=200)




class BookInstance(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    imprint=models.CharField(max_length=200,blank=True)
    due_back=models.DateField(null=True,blank=True)
    borrower=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    RETURN_STATUS = (
        ('r', 'Return'),
        ('c', 'Confirm'),
        ('f','Fake request'),
    )

    LOAN_STATUS=(
        ('m','Maintainance'),
        ('o','On_loan'),
        ('a','Available'),
        ('r','Reserved'),

    )
    status=models.CharField(max_length=1,choices=LOAN_STATUS,default='a')
    rtn_status = models.CharField(max_length=1, choices=RETURN_STATUS, null=True, blank=True)

    @property
    def is_overdue(self):
       if date.today()>self.due_back:
            return  True
       return False

    class Meta:
        ordering=["due_back"]
        permissions=(("lib_perms","librarian permissions"),("manage_books","book management"))

    def __str__(self):
        return  '%s'%(self.id)


@receiver(post_save,sender=Book)
def ensure_bookinstance(sender, **kwargs):
    bk=kwargs.get('instance')
    ct=BookInstance.objects.filter(book=bk).count()
    status=kwargs.get('created',False)

    if bk.no_instance > ct:
        for i in range(bk.no_instance-ct):
            BookInstance.objects.create(book=bk)

    # not working recurrsion error
    #else:
     #   bk.no_instance=ct
      #  bk.save()

@receiver(post_save,sender=IssueRequest)
def give_notification(sender, **kwargs):
    requ=kwargs.get('instance')
    book=requ.book
    status=kwargs.get('created',False)
    if requ.status == 'a':
        Ins_A = BookInstance.objects.filter(book=book).filter(status__exact='a')[0]
        Ins_A.status='o'
        Ins_A.borrower =requ.user
        Ins_A.due_back=requ.return_date
        Ins_A.save()
        Notification.objects.create(user=requ.user,notice="'%s' has been issued to you on your request " % requ.book.title)
    if requ.status == 'r':
        Notification.objects.create(user=requ.user, notice="Your request to issue '%s' has been rejected" % requ.book.title)



