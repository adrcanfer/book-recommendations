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
