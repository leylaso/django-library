# -*- coding: utf-8 -*- 

from library.models import *
from django.contrib import admin

class LoanInline(admin.TabularInline):
  model = Loan
  extra = 1

class BookAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['title', 'subtitle', 'description', 'author', 'category', 'language', 'lost']}),
    ('Numéros de référence', {'fields': ['isbn', 'oclc', 'lccn', 'olid'], 'classes': ['collapse']}),
    ('Liens', {'fields': ['olink', 'cover', 'ebook'], 'classes': ['collapse']}),
  ]
  inlines = [LoanInline]
  list_display = ('title', 'available', 'category', 'language')
  list_filter = ['category', 'language']

class BorrowerAdmin(admin.ModelAdmin):
  inlines = [LoanInline]
  list_display = ('name', 'email', 'phone')

admin.site.register(Book, BookAdmin)
admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Loan)
