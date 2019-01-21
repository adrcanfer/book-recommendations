import os
import shutil
import time
import shelve
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from main import scrapping
from main import models
from main import indexWhoosh
from .forms import searchForm, idForm, registerForm, loginForm, ratingForm
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from .models import Book, Rating, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    models.User.objects.all().delete()
    for user in range(6):
        userCreated = models.User.objects.create(username="user" + str(user + 1), password="user" + str(user + 1))
        for rating in range(20):
            if user == 0:
                aux_rating(userCreated, rating, "Contemporánea")
            elif user == 1:
                aux_rating(userCreated, rating, "Negra")
            elif user == 2:
                aux_rating(userCreated, rating, "Romántica")
            elif user == 3:
                aux_rating(userCreated, rating, "Cómics")
            elif user == 4:
                aux_rating(userCreated, rating, "Historia")
            elif user == 5:
                aux_rating(userCreated, rating, "Adolescentes")
            elif user == 6:
                aux_rating(userCreated, rating, "Infantil")
    stop = time.time()
    return HttpResponse(str(stop - start))


def aux_rating(user, rating, category):
    if rating < 10:
        categorybooks = models.Book.objects.filter(category=category)
        models.Rating.objects.create(user=user, book=categorybooks[rating], rating=10)
    else:
        nocategorybooks = models.Book.objects.exclude(category=category)
        models.Rating.objects.create(user=user, book=nocategorybooks[rating - 10], rating=2)


def list_book(request):
    books_all = models.Book.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(books_all, 10)

    try:
        books = paginator.page(page)
    except PageNotAsInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.age(paginator.num_pages)

    return render(request, 'list_book.html', {'books': books})


def search(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["buscar"]
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
    return HttpResponse(str(stop - start))


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


def create_user(request):
    res = None
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
            res = HttpResponseRedirect("/")
        else:
            res = render(request, 'create.html', {'form': form, 'sendButton': "Crear usuario"})
    else:
        form = registerForm()
        res = render(request, 'create.html', {'form': form, 'sendButton': "Crear usuario"})

    return res


def login(request):
    res = None
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = models.User.objects.filter(username=username, password=password)
            for u in user:
                request.session['loggedId'] = u.id
            res = HttpResponseRedirect("/")
        else:
            res = render(request, 'create.html', {'form': form, 'sendButton': "Iniciar sesión"})
    else:
        form = loginForm()
        res = render(request, 'create.html', {'form': form, 'sendButton': "Iniciar sesión"})
    return res


def logout(request):
    request.session['loggedId'] = -1
    return HttpResponseRedirect("/")


def rating(request):
    if request.method == 'POST':
        loggedId = request.session.get('loggedId', None)
        if loggedId is None or loggedId == '':
            return HttpResponseRedirect('/')
        form = ratingForm(request.POST)
        if form.is_valid():
            bookId = form.cleaned_data['bookId']
            if bookId is None or bookId == '':
                return HttpResponseRedirect('/')
            rat = form.cleaned_data['rating']
            userId = request.session['loggedId']
            user = get_object_or_404(User, id= userId)
            book = get_object_or_404(Book, id=bookId)
            count = Rating.objects.filter(book=book, user=user).count()
            if count > 0:
                return render(request, 'rated.html', {})
            Rating.objects.create(user=user, book=book, rating=rat)
            return render(request, 'thanks.html', {})
    else:
        loggedId = request.session.get('loggedId', None)
        if loggedId is None or loggedId == '':
            return HttpResponseRedirect('/')
        bookId = request.GET.get('q', None)
        if bookId is None or bookId == '':
            return HttpResponseRedirect('/')
        b = get_object_or_404(Book, id=bookId)
        user = get_object_or_404(User, id=loggedId)
        count = Rating.objects.filter(book=b, user=user).count()
        if count > 0:
            return render(request, 'rated.html', {})
        form = ratingForm(initial={'bookId': bookId})
        return render(request, 'rating.html', {'name': b.title, 'form': form})
