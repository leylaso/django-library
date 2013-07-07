from django.conf.urls.defaults import patterns, include, url
from library.models import *
from django.views.generic import DetailView, ListView
from django.contrib import admin
from library.admin import *

urlpatterns = patterns('library.views',
  url(r'^api/makePublisher/', 'makePublisher'),
  url(r'^api/makeAuthor/', 'makeAuthor'),
  url(r'^api/searchISBN/', 'searchISBN'),
  url(r'^api/getISBN/', 'getISBN'),
  url(r'^admin/library/loan/$', 'lateLoans'),

  url(r'^$', 'booksBy'),
  url(r'^bk$', 'booksBy'),

  url(r'^bk/(?P<pk>\d+)/$', 'book'),

  url(r'^bk/(?P<args>.+)/$', 'booksBy'),
  url(r'^admin/', include(admin.site.urls)),
)
