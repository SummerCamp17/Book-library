from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book,Author,Genre,BookInstance,IssueRequest,Notification
from django.contrib.auth.decorators import login_required ,permission_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .filters import BookFilter


# Create your views here.
def book_filter(request):
    f = BookFilter(request.GET, queryset=Book.objects.all())
    return render(request, 'book_filter.html', {'filter': f})


def index(request):
    books = Book.objects.all()
    all_books = books[::-1]
    added_books=all_books[:6]
    return render(request,'index.html',context={'added_books':added_books})

@login_required
def notifications(request):
    return render(request,'notice.html')


@login_required
def books(request):
    books=Book.objects.all()
    all_books=books[::-1]
    return render(request,'books.html',context={'all_books':all_books})

def detail(request,pk):
    book=Book.objects.get(pk=pk)
    insA=BookInstance.objects.filter(book=book).filter(status__exact='a').count()
    return render(request, 'book_detail.html', context={'book': book,'insA':insA})

from .forms import RequestIssueForm,RegistrationForm

@login_required
def req_issue(request,pk):
    book = Book.objects.get(pk=pk)
    Ins = BookInstance.objects.filter(book=book).filter(status__exact='a')
    ct = Ins.count()
    dub=BookInstance.objects.filter(book=book).filter(borrower=request.user)
    k=0
    if dub:
        k=1
        form="This book is currently issued to you.You can't make a request to issue a book that is already currenty issued to you"
    else:
        if request.method=='POST':
            form=RequestIssueForm(request.POST)
            if form.is_valid():
                IssueRequest.objects.create(user=request.user, book=book, return_date=form.cleaned_data['return_date'])
                Notification.objects.create(user=request.user,notice="Your request to issue '%s' has been sent for review" %book.title)

                return HttpResponseRedirect(reverse('books'))

        else:
            form=RequestIssueForm()

    return render(request, 'request_issue.html', context={'form':form,'ct':ct,'book':book,'k':k})


@login_required
def authors(request):
    all_authors = Author.objects.all()
    return render(request, 'authors.html', context={'all_authors': all_authors})


@login_required
def genre(request):
    genre = Genre.objects.all()
    return render(request, 'genre.html', context={'genre': genre})


@login_required
def loaned_book_by_user(request):
    all_loaned=BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').exclude(rtn_status__exact='r').order_by('due_back')
    issue=IssueRequest.objects.filter(user=request.user).filter(status__exact='n')
    rtn=BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').filter(rtn_status__exact='r').order_by('due_back')
    return  render(request,'my_books.html',context={'borrowed':all_loaned,'rtn':rtn,'issue':issue})


@login_required
def return_book(request,pk):
    Ins = BookInstance.objects.filter(borrower=request.user).get(pk=pk)
    if Ins.rtn_status=='r':
        Ins.rtn_status =None
        Ins.save()
        Notification.objects.create(user=request.user,notice="You successfully took back '%s' book return request" % Ins.book.title)
    else:
        Ins.rtn_status='r'
        Ins.save()
        Notification.objects.create(user=request.user,notice="Your claim to return '%s' book is waiting for confirmation" % Ins.book.title)
    return HttpResponseRedirect(reverse('my_books'))


@permission_required('mylib.manage_books')
def all_issued_book(request):
    all_issued=BookInstance.objects.filter(status__exact='o').order_by('due_back','borrower')
    return  render(request,'issued_books.html',context={'issued':all_issued})


@permission_required('mylib.manage_books')
def request_list(request):
    request_list=IssueRequest.objects.filter(status__exact='n')
    return  render(request,'request_list.html',context={'list':request_list})


@permission_required('mylib.manage_books')
def return_claims(request):
    claim_list=BookInstance.objects.filter(status__exact='o').filter(rtn_status__exact='r')
    return  render(request,'claim_list.html',context={'list':claim_list})


@login_required
@permission_required('mylib.manage_books')
def confirm_claim(request,pk):
    Ins = BookInstance.objects.get(pk=pk)
    Notification.objects.create(user=Ins.borrower,notice="Your claim to return '%s' book is approved " % Ins.book.title)
    Ins.rtn_status=None
    Ins.status='a'
    Ins.borrower=None
    Ins.due_back=None
    Ins.save()

    return HttpResponseRedirect(reverse('return_claims'))


@login_required
@permission_required('mylib.manage_books')
def fake_claim(request,pk):
    Ins = BookInstance.objects.get(pk=pk)
    Ins.rtn_status=None
    Ins.save()
    Notification.objects.create(user=Ins.borrower,notice="Your claim to return '%s' book has been found fake. " % Ins.book.title)
    return HttpResponseRedirect(reverse('return_claims'))





class BookCreate(CreateView):
    model=Book
    fields='__all__'
    success_url=reverse_lazy('books')



class BookUpdate(UpdateView):
    model=Book
    fields=['author','description',]


class IssueRequestUpdate(UpdateView):
    model= IssueRequest
    fields='__all__'
    success_url = reverse_lazy('request_list')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            return HttpResponseRedirect('/accounts/login')
    else:
        form = RegistrationForm()
    return render(request,'sign_in.html',context={'form':form})
