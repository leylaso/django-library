# -*- coding: utf-8 -*- 

from library.models import *
from django.contrib import admin

class LoanInline(admin.TabularInline):
  model = Loan
  extra = 1
  raw_id_fields = ('book', 'borrower')

class BookInline(admin.TabularInline):
  model = Book
  extra = 1
  fields = ['__unicode__', 'publisher', 'year', 'category']

class BookAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['title', 'subtitle', 'description', 'author', 'publisher', 'year', 'category', 'genre', 'language', 'lost']}),
    ('Numéros de référence', {'fields': ['isbn', 'oclc', 'lccn', 'olid'], 'classes': ['collapse']}),
    ('Liens', {'fields': ['olink', 'cover', 'ebook'], 'classes': ['collapse']}),
  ]
  list_filter = ['language', 'category', 'publisher', 'author']
  inlines = [LoanInline]
  list_display = ('__unicode__', 'available', 'category', 'language')
  search_fields = ['title', 'subtitle', 'author__surname', 'author__givenames', 'publisher__name', 'category__title'] 
  raw_id_fields = ['author', 'publisher']

class BorrowerAdmin(admin.ModelAdmin):
  inlines = [LoanInline]
  list_display = ('name', 'email', 'phone')
  search_fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
  search_fields = ['surname', 'givenames']

class PublisherAdmin(admin.ModelAdmin):
  search_fields = ['name']

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Category)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Loan)
