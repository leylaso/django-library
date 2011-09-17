# -*- coding: utf-8 -*- 

from django.shortcuts import render_to_response, get_object_or_404
from library.models import Loan
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
import datetime

def lateLoans(request):
  return render_to_response(
    'admin/library/lateloans.html',
    {'loans' : Loan.objects.filter(returned__isnull=True, due__lt=datetime.date.today())},
    RequestContext(request, {}),
  )

lateLoans = staff_member_required(lateLoans)
