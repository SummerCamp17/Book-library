from django.conf.urls import url

from . import views
urlpatterns =[
    url(r'^$',views.index,name='index'),
    url(r'^books/$',views.books,name='books'),
    url(r'^books/(?P<pk>\d+)/$',views.detail,name='book_detail'),
    url(r'^books/(?P<pk>\d+)/request_issue/$',views.req_issue,name='request_issue'),

    url(r'^books/(?P<pk>[0-9a-f-]+)/request_issue/confirm/$',views.IssueRequestUpdate.as_view(),name='confirm_issue'),
    url(r'^authors/$',views.authors,name='authors'),
    url(r'^mybooks/$',views.loaned_book_by_user,name='my_books'),
    url(r'^mybooks/(?P<pk>[0-9a-f-]+)/return/$',views.return_book,name='return_book'),
    url(r'^issued/$',views.all_issued_book,name='issued_books'),
    url(r'^request_list/$',views.request_list,name='request_list'),
    url(r'^return_claims/$',views.return_claims,name='return_claims'),
    url(r'^return_claims/(?P<pk>[0-9a-f-]+)/confirm/$', views.confirm_claim, name='confirm_claim'),
    url(r'^return_claims/(?P<pk>[0-9a-f-]+)/fake/$', views.fake_claim, name='fake_claim'),
    url(r'^books/create/$',views.BookCreate.as_view(),name='book_create'),
    url(r'^books/(?P<pk>\d+)/update/$',views.BookUpdate.as_view(),name='book_update'),
    url(r'^books/notifications/$',views.notifications,name='notifications'),

]


