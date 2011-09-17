# -*- coding: utf-8 -*- 

from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
  title = models.CharField(max_length=256)
  description = models.TextField('Description', blank=True)
  def __unicode__(self):
    return self.title

class Author(models.Model):
  surname = models.CharField(max_length=256)
  givenames = models.CharField(max_length=256)
  def __unicode__(self):
    return self.givenames + ' ' + self.surname

class Book(models.Model):
  title = models.CharField(max_length=256)
  subtitle = models.CharField(max_length=256)
  description = models.TextField('Description', blank=True)
  isbn = models.CharField(max_length=24, blank=True)
  oclc = models.CharField(max_length=24, blank=True)
  lccn = models.CharField(max_length=24, blank=True)
  olid = models.CharField(max_length=24, blank=True)
  language = models.CharField(max_length=3, choices= (
    ('MUL', 'Plusieurs/Bilingue'),
    ('fra', 'Français'),
    ('eng', 'Anglais'),
    ('esp', 'Espagnol'),
    ('AUT', 'Autre'),
  ))
  category = models.ForeignKey(Category, blank=True, null=True)
  author = models.ForeignKey(Author, blank=True, null=True)
  def __unicode__(self):
    return self.title

class Borrower(models.Model):
  name = models.CharField(max_length=256)
  email = models.EmailField(max_length=256, blank=True)
  phone = models.CharField(max_length=24, blank=True)
  notes = models.TextField('Description', blank=True)
  def __unicode__(self):
    return self.name

class Loan(models.Model):
  book = models.ForeignKey(Book)
  borrower = models.ForeignKey(Borrower)
  borrowed = models.DateField("Date de l'empreunt")
  due = models.DateField("Date prévue de retour")
  returned = models.DateField("Date actuel du retour", blank=True)
  def __unicode__(self):
    return self.borrower + ': ' + self.book
  def is_late(self):
    return self.due <= datetime.date.today()
      
