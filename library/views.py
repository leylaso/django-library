# -*- coding: utf-8 -*- 

from django.shortcuts import render_to_response, get_object_or_404
from library.models import * 
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def lateLoans(request):
  return render_to_response(
    'admin/library/lateloans.html',
    {'loans' : Loan.objects.filter(returned__isnull=True, due__lt=datetime.date.today())},
    RequestContext(request, {}),
  )

lateLoans = staff_member_required(lateLoans)

def booksBy(request, args=''):
  filters = []
  active = {}
  if args:
    conds = args.split('/')
    args = '/' + args
    for arg in conds:
      arg = arg.split(':')
      filters += [arg[0] + '="' + arg[1] + '"']
      active[arg[0]] = arg[1]
    filters = ', '.join(filters)
    bookQuery = 'Book.objects.filter(' + filters + ')'
  else: 
    bookQuery = 'Book.objects.all()'
  exec "books = " + bookQuery

  pagedBook = Paginator(books, 50)
  curPage = request.GET.get('page')

  if curPage:
    try:
      bookPage = pagedBook.page(curPage)
    except PageNotAnInteger:
      bookPage = pagedBook.page(1)
    except EmptyPage:
      bookPage = pagedBook.page(pagedBook.num_pages)
  else:
    bookPage = pagedBook.page(1)

  language = {}
  for book in books:
    if language.has_key(book.language):
      language[book.language]['count'] += 1
    else:
      language[book.language]= {'count': 1, 'text': book.language, 'link': '/bk' + args + '/language:' + book.language}

  category = {}
  for book in books:
    if category.has_key(str(book.category.id)):
      category[str(book.category.id)]['count'] += 1
    else:
      category[str(book.category.id)] = {'count': 1, 'text': book.category.title, 'link': '/bk' + args + '/category:' + str(book.category.id)}

  author = {}
  for book in books:
    if author.has_key(str(book.author.id)):
      author[str(book.author.id)]['count'] += 1
    else:
      author[str(book.author.id)] = {'count': 1, 'text': book.author.__unicode__, 'link': '/bk' + args + '/author:' + str(book.author.id)}
  
  for act, val in active.items():
    exec 'active[act] = ' + act + '["' + active[act] + '"]'
    active[act]['cond'] = val
    exec act + ' = None'
  for act in active:
    link = '/bk'
    for a in active:
      if a != act:
        link += '/' + a + ':' + active[a]['cond']
    active[act]['link'] = link

  

  return render_to_response('library/bookSearch.html',
    {'books': bookPage, 'langs': language, 'cats': category, 'auths': author, 'active': active})
