import csv
from library.models import *
import re
import os

def clearDB():
  # TODO make sure to purge secret data from here before committing this!
  os.system("mysql -u dira_library -p dira_library < trash.sql")

def csvOpen(csvfile, delimiter="\t", quotechar='"'):
  return csv.reader(open(csvfile, 'rb'), delimiter=delimiter, quotechar=quotechar)

def saveBook(row, language):
  return ''

def saveCat(category):
  cat = Category.objects.filter(title=category)
  if cat:
    return cat[0]
  else:
    cat = Category(title=category)
    cat.save()
    return cat

def saveAuthor(sur, give = ''):
  auth = Author.objects.filter(surname=sur, givenames=give)
  if auth:
    return auth[0]
  else:
    auth = Author(surname=sur, givenames=give)
    auth.save()
    return auth

def savePub(name):
  pub = Publisher.objects.filter(name=name)
  if pub:
    return pub[0]
  else:
    pub = Publisher(name=name)
    pub.save()
    return pub

def printLine(row, ofile = 'output.csv'):
  of = open(ofile, 'a')
  line = "\t".join(row)
  of.write(line + "\n")
  of.close

def process(csv, fields = ['author', 'title', 'year', 'publisher'], language='eng', category='Anarchism'):
  # First save the category if necessary
  cat = saveCat(category)
  valid = 0
  for row in csv:
    if rowLength(row) > 0:
      if validRow(row, fields):
        valid += 1
        count = 0
        book = {}
        while count < len(fields):
          book[fields[count]] = row[count]
          print fields[count] + " " + row[count] + "  ."
          count += 1
        print "\n"
        # Save the category if available
        if book.has_key('category'):
          cat = saveCat(book['category'])

        # Save the author
        authNames = book['author'].split(',')
        if len(authNames) > 1:
          auth = saveAuthor(authNames[0].strip(), authNames[1].strip())
        elif len(authNames) == 1:
          auth = saveAuthor(authNames[0].strip())

        # Save the publisher
        if len(book['publisher']) > 0:
          pub = savePub(book['publisher'])

        try:
          book = Book(title=book['title'], year=book['year'], category=cat, publisher=pub, language=language)
          book.save()
          book.author.add(auth)
          book.save()
        except:
          printLine(row)
      else:
        printLine(row)
  return str(valid) + " rows imported\n"
    

def validInfo(csv, fields = ['author', 'title', 'year', 'publisher', 'genre']):
  valid = 0
  invalid = 0
  empty = 0
  for row in csv:
    if rowLength(row) == 0:
      empty += 1
    elif validRow(row, fields):
      valid += 1
    else:
      invalid += 1
  return str(valid) + " valid rows\n" + str(invalid) + " invalid rows\n" + str(empty) + " empty rows\n"

def rowLength(row):
  length = 0
  for field in row:
    length += len(field)
  return length

def validRow(row, fields = ['author', 'title', 'year', 'publisher', 'genre']):
  count = 0
  validFields = 0
  while count < len(fields):
    exec 'if ' + fields[count] + 'Valid(row[count]): validFields += 1'
    count += 1
  if validFields == len(fields):
    return True
  else:
    return False

def authorValid(text):
  return re.match('^[^, ]*[^,]+[, ]+[^,]+$', text)

def titleValid(text):
  return len(text) < 257

def yearValid(text):
  return len(text) < 5

def publisherValid(text):
  return len(text) < 257

def genreValid(text):
  return len(text) < 257

def categoryValid(text):
  return len(text) < 257
