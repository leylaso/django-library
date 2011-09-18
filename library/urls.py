from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from library.models import *

urlpatterns = patterns('library.views',

  url(r'^loan$', 'lateLoans'),
  url(r'^loan/$', 'lateLoans'),

)
