from django.shortcuts import render, HttpResponse
from main import scrapping
from main import models
import time


def index(request):
    return render(request, 'index.html')


def populate(request):
    start = time.time()
    models.Book.objects.all().delete()
    scrapping.scrapContemporany()
    scrapping.scrapBlack()
    stop = time.time()
    return HttpResponse(str(stop - start))


def booklist(request):
    books = models.Book.objects.all()
    return render(request, 'booklist.html', {'books': books})

