from django.conf.urls.defaults import patterns, include, url
from library.models import *

urlpatterns = patterns('library.views',

  url(r'^admin/library/loan/$', 'lateLoans'),

)
