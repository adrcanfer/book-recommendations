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


def generate_rating(request):
    start = time.time()
    models.Rating.objects.all().delete()
    for user in range(2):
        for rating in range(20):
            if user == 0:
                if rating < 10:
                    contemporanybooks = models.Book.objects.filter(category="Contemporánea")
                    models.Rating.objects.create(userId=user + 1, book=contemporanybooks[rating], rating=10)
                else:
                    nocontemporanybooks = models.Book.objects.exclude(category="Contemporánea")
                    models.Rating.objects.create(userId=user + 1, book=nocontemporanybooks[rating - 10], rating=3)
            elif user == 1:
                if rating < 10:
                    blackbooks = models.Book.objects.filter(category="Negra")
                    models.Rating.objects.create(userId=user + 1, book=blackbooks[rating], rating=10)
                else:
                    noblackbooks = models.Book.objects.exclude(category="Negra")
                    models.Rating.objects.create(userId=user + 1, book=noblackbooks[rating - 10], rating=2)
    stop = time.time()
    return HttpResponse(str(stop - start))


def list_book(request):
    books = models.Book.objects.all()
    return render(request, 'list_book.html', {'books': books})
