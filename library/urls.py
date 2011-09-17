from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from library.models import *

urlpatterns = patterns('library.admin_views',

  url(r'^lateloans$', 'lateLoans'),

)
