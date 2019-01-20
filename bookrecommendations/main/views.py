import os
import shutil
from django.shortcuts import render, HttpResponse
from main import scrapping
from main import models
import time
from .forms import searchForm, idForm
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from main import indexWhoosh
import shelve


def index(request):

    return render(request, 'index.html')


def populate(request):
    start = time.time()
    if os.path.exists("booksIndex"):
        shutil.rmtree("booksIndex")
    models.Book.objects.all().delete()
    scrapping.scrap('https://www.casadellibro.com/libros/novela-contemporanea/128000000', 'Contemporánea')
    scrapping.scrap('https://www.casadellibro.com/libros/romantica-y-erotica/narrativa-romantica/127000000',
                    'Romántica')
    scrapping.scrap('https://www.casadellibro.com/libros/novela-negra/126000000', 'Negra')
    scrapping.scrap('https://www.casadellibro.com/libros/narrativa-historica/125000000', 'Historia')
    scrapping.scrap('https://www.casadellibro.com/libros/comics-adultos/411000000', 'Cómics')
    scrapping.scrap('https://www.casadellibro.com/libros/juvenil/117001014', 'Adolescentes')
    scrapping.scrap('https://www.casadellibro.com/libros/infantil/117000000', 'Infantil')
    indexWhoosh.indexBooks()
    stop = time.time()
    return HttpResponse(str(stop - start))


def generate_rating(request):
    start = time.time()
    models.Rating.objects.all().delete()
    for user in range(6):
        for rating in range(20):
            if user == 0:
                aux_rating(user + 1, rating, "Contemporánea")
            elif user == 1:
                aux_rating(user + 1, rating, "Negra")
            elif user == 2:
                aux_rating(user + 1, rating, "Romántica")
            elif user == 3:
                aux_rating(user + 1, rating, "Cómics")
            elif user == 4:
                aux_rating(user + 1, rating, "Historia")
            elif user == 5:
                aux_rating(user + 1, rating, "Adolescentes")
            elif user == 6:
                aux_rating(user + 1, rating, "Infantil")
    stop = time.time()
    return HttpResponse(str(stop - start))


def aux_rating(userid, rating, category):
    if rating < 10:
        blackbooks = models.Book.objects.filter(category=category)
        models.Rating.objects.create(userId=userid, book=blackbooks[rating], rating=10)
    else:
        noblackbooks = models.Book.objects.exclude(category=category)
        models.Rating.objects.create(userId=userid, book=noblackbooks[rating - 10], rating=2)


def list_book(request):
    books = models.Book.objects.all()
    return render(request, 'list_book.html', {'books': books})


def search(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["query"]
            books = []
            ix = open_dir("booksIndex")
            with ix.searcher() as searcher:
                qp = MultifieldParser(["title", "author", "editorial", "synopsis"], schema=ix.schema).parse(q.upper())
                results = searcher.search(qp)
                for r in results:
                    books.append(models.Book.objects.get(id=r["id"]))

            return render(request, 'list_book.html', {'books': books})
    else:
        form = searchForm()

    return render(request, 'search.html', {'form': form})


def load_rs(request):
    start = time.time()
    shelf = shelve.open('dataRS.dat')
    users = models.Rating.objects.values('userId').distinct()
    userrecom = {}
    for user in users:
        idusu = user['userId']
        ratings = models.Rating.objects.filter(userId=idusu)
        books = models.Book.objects.all()
        userrecom.setdefault(idusu, [])
        bookrecom = {}
        for book in books:
            if ratings.filter(book=book.id).first() is None:
                puntu = 0
                for rating in ratings:
                    ratpuntu = 0
                    if rating.book.category == book.category:
                        ratpuntu += 3
                    if rating.book.author == book.author:
                        ratpuntu += 2
                    ratpuntu *= rating.rating
                    puntu += ratpuntu
                bookrecom[book.id] = puntu
        sortedrecom = sorted(bookrecom.items(), key=lambda x: x[1], reverse=True)[:10]
        userrecom[idusu] = sortedrecom
    shelf['userrecom'] = userrecom
    shelf.close()
    stop = time.time()
    return HttpResponse(str(stop-start))


def recommendations(request):
    if request.method == 'POST':
        form = idForm(request.POST)
        if form.is_valid():
            idusu = form.cleaned_data['userId']
            shelf = shelve.open('dataRS.dat')
            recom = shelf['userrecom'][idusu]
            books = []
            for recommendation in recom:
                book = models.Book.objects.filter(id=recommendation[0]).first()
                books.append(book)
            return render(request, 'list_book.html', {'books': books})
    else:
        form = idForm()
    return render(request, 'search.html', {'form': form})
