# -*- coding: utf-8 -*- 

from django.shortcuts import render_to_response, get_object_or_404
from library.models import * 
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import datetime

def lateLoans(request):
  return render_to_response(
    'admin/library/lateloans.html',
    {'loans' : Loan.objects.filter(returned__isnull=True, due__lt=datetime.date.today())},
    RequestContext(request, {}),
  )

lateLoans = staff_member_required(lateLoans)

def getISBN(request):
    q = request.GET.get('term', '')
    results = []
    ojson = {}
    ojson['label'] = '1234567891'
    ojson['value'] = 'le livre !'
    results.append(ojson)
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)	

def book(request, pk):
  book = get_object_or_404(Book, pk=pk)
  if book.not_available():
    messages = [{'class': 'warning', 'text': "Ce livre n'est pas disponible"}]
  else:
    messages = None
  return render_to_response('library/book.html', {'book': book, 'messages': messages})

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
  exec "books = " + bookQuery + '.order_by("id").reverse()'

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

  actives = {}
  facets = {}

  language = {}
  if active.has_key('language'):
    langSorted = None
    actives['language'] = {'text': active['language']}
  else:
    exec "langs = " + bookQuery + ".values('language').annotate(Count('title'))"
    for lang in langs:
      language[lang['language']] = {'count': lang['title__count'], 'text': lang['language'], 'link': '/bk' + args + '/language:' + lang['language']}
    langKeys = language.keys()
    langKeys.sort()
    langSorted = map(language.get, langKeys)  
  if langSorted:
    facets['Language'] = langSorted

  category = {}
  if active.has_key('category'):
    catSorted = None
    cat = Category.objects.get(id=active['category'])
    actives['category'] = {'text': cat.title, 'link': '/bk' + args + '/category:' + str(cat.id)}
  else:
    exec "cats = " + bookQuery + ".values('category__id', 'category__title').annotate(Count('title'))"
    for cat in cats:
      category[cat['category__title']] = {'count': cat['title__count'], 'text': cat['category__title'], 'link': '/bk' + args + '/category:' + str(cat['category__id'])}    
    catKeys = category.keys()
    catKeys.sort()
    catSorted = map(category.get, catKeys)
  if catSorted:
    facets['Section'] = catSorted

  if active.has_key('author'):
    auth = Author.objects.get(id=active['author'])
    actives['author'] = {'text': auth.__unicode__, 'link': '/bk' + args + '/author:' + str(auth.id)}

  if active.has_key('publisher'):
    pub = Publisher.objects.get(id=active['publisher'])
    actives['publisher'] = {'text': pub.__unicode__, 'link': '/bk' + args + '/publisher:' + str(pub.id)}

  for act in active:
    link = '/bk'
    for a, val in active.items():
      if a != act:
        link += '/' + a + ':' + val
    actives[act]['link'] = link

  return render_to_response('library/bookSearch.html',
    {'books': bookPage, 'facets': facets, 'active': actives})
