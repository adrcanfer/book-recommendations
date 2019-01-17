from django.shortcuts import render, HttpResponse
from main import scrapping
import time


def index(request):
    return render(request, 'index.html')

def populate(request):
    inicio = time.time()
    scrapping.scrapContemporany()
    fin = time.time()
    return HttpResponse(str(fin - inicio))
