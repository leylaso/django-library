# -*- coding: utf-8 -*- 

from django.db import models
import datetime
import simplejson
import pycurl
import StringIO
import re

# Create your models here.
class Topic(models.Model):
  title = models.CharField(max_length=256, verbose_name='Titre')
  related_topics = models.ManyToManyField('library.Topic', blank=True, null=True, verbose_name='Sujets reliés', related_name='related_topics_f')
  subtopics = models.ManyToManyField('library.Topic', blank=True, null=True, verbose_name='Sous-Sujets', related_name='subtopics_f')
  description = models.TextField(verbose_name='Déscription', blank=True)
  def __unicode__(self):
    return self.title

class Category(models.Model):
  title = models.CharField(max_length=256, verbose_name='Titre')
  description = models.TextField(verbose_name='Déscription', blank=True)
  def __unicode__(self):
    return self.title

class Publisher(models.Model):
  name = models.CharField(max_length=256, verbose_name='Nom')
  link = models.URLField(max_length=256, blank=True, verbose_name="Lien vers l'éditeur.")
  description = models.TextField(verbose_name='Déscription', blank=True)
  def __unicode__(self):
    return self.name

class Author(models.Model):
  surname = models.CharField(max_length=256, verbose_name='Nom')
  givenames = models.CharField(max_length=256, verbose_name='Prénoms', blank=True)
  olid = models.CharField(max_length=24, blank=True, verbose_name='OLID')
  def __unicode__(self):
    if self.givenames:
      return self.surname + ', ' + self.givenames
    else:
      return self.surname

class Book(models.Model):
  title = models.CharField(max_length=256, verbose_name='Titre')
  subtitle = models.CharField(max_length=256, blank=True, verbose_name='Sous-titre')
  description = models.TextField(verbose_name='Description', blank=True)
  isbn = models.CharField(max_length=24, blank=True, verbose_name='ISBN')
  oclc = models.CharField(max_length=24, blank=True, verbose_name='OCLC')
  lccn = models.CharField(max_length=24, blank=True, verbose_name='LCCN')
  olid = models.CharField(max_length=24, blank=True, verbose_name='OLID')
  olink = models.URLField(max_length=256, blank=True, verbose_name='Lien vers Open Library')
  cover = models.URLField(max_length=256, blank=True, verbose_name='Lien vers une image de la couverture')
  ebook = models.URLField(max_length=256, blank=True, verbose_name='Lien vers une version éléctronique')
  topics = models.ManyToManyField('library.Topic', blank=True, null=True, verbose_name='Sujets')
  language = models.CharField(max_length=3, choices= (
    ('MUL', 'Plusieurs/Bilingue'),
    ('fra', 'Français'),
    ('eng', 'Anglais'),
    ('esp', 'Espagnol'),
    ('AUT', 'Autre'),
  ))
  category = models.ForeignKey(Category, blank=True, null=True, verbose_name='Section')
  author = models.ManyToManyField(Author, blank=True, null=True, verbose_name='Auteur')
  year = models.CharField(max_length=4, blank=True, verbose_name='Année') 
  publisher = models.ForeignKey(Publisher, blank=True, null=True, verbose_name="Maison d'édition")
  genre = models.CharField(max_length=256, blank=True, verbose_name='Genre')
  lost = models.BooleanField(default=False, verbose_name='Ce livre est perdu')
  def __unicode__(self):
    if self.subtitle:
      return self.title + ': ' + self.subtitle
    else:
      return self.title
  def not_available(self):
    if self.lost:
      return self.lost
    else:
      loans = self.loan_set.values('returned')
      result = False
      for line in loans:
        if line['returned'] is None:
          result = True
      return result
  def available(self):
    if self.not_available():
      return False
    else:
      return True
  def sanitize_isbn(self):
    if self.isbn:
      pattern = re.compile('[^0-9]')
      return pattern.sub('', self.isbn)
  def fetch_olrecord(self):
    if self.isbn:
      curlReq = pycurl.Curl()
      burl = 'http://openlibrary.org/api/books?bibkeys=ISBN:' + self.sanitize_isbn() + '&format=json&jscmd=data'
      curlReq.setopt(pycurl.URL, burl.__str__())
      curlReq.setopt(pycurl.FOLLOWLOCATION, 1)
      curlReq.setopt(pycurl.MAXREDIRS, 5)
      book = StringIO.StringIO()
      curlReq.setopt(pycurl.WRITEFUNCTION, book.write)
      curlReq.perform()
      book = StringIO.StringIO(book.getvalue())
      book = simplejson.load(book)
      return book[book.keys()[0]]

class Borrower(models.Model):
  name = models.CharField(max_length=256, verbose_name='Nom')
  email = models.EmailField(max_length=256, blank=True, verbose_name='Courriel')
  phone = models.CharField(max_length=24, blank=True, verbose_name='Téléphone')
  notes = models.TextField(blank=True, verbose_name='Notes')
  def __unicode__(self):
    return self.name

class Loan(models.Model):
  book = models.ForeignKey(Book, verbose_name='Livre')
  borrower = models.ForeignKey(Borrower, verbose_name='Emprunteur')
  borrowed = models.DateField(verbose_name="Date de l'emprunt")
  due = models.DateField(verbose_name="Date prévue de retour")
  returned = models.DateField(verbose_name="Date actuel du retour", blank=True, null=True)
  def __unicode__(self):
    return str(self.book) + ' (' + str(self.borrowed) + ' - ' + str(self.returned) + ')'
  def is_late(self):
    if self.returned is None:
      return self.due <= datetime.date.today()
    else:
      return False
      
