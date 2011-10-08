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
  fields = ['title', 'publisher', 'year', 'category']

class BookAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['title', 'subtitle', 'description', 'author', 'publisher', 'year', 'category', 'genre', 'language', 'lost']}),
    ('Numéros de référence', {'fields': ['isbn', 'oclc', 'lccn', 'olid'], 'classes': ['collapse']}),
    ('Liens', {'fields': ['olink', 'cover', 'ebook'], 'classes': ['collapse']}),
  ]
  inlines = [LoanInline]
  list_display = ('title', 'available', 'category', 'language')
  list_filter = ['category', 'language', 'author']
  search_fields = ['title']
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
