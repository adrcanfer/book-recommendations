import urllib.request

from bs4 import BeautifulSoup
from main.models import Book


def scrapContemporany():
    total = 0
    f = urllib.request.urlopen('https://www.casadellibro.com/libros/novela-contemporanea/128000000')
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('span', class_='fnt09im').text.split(" ")[3]
    for i in range(int(pages)):
        f = urllib.request.urlopen('https://www.casadellibro.com/libros/novela-contemporanea/128000000/p' + str(i + 1))
        html = f.read()
        f.close()
        soup = BeautifulSoup(html, 'lxml')
        books = soup.find_all('div', class_='mod-list-item')
        for book in books:
            title = book.find('a', class_='title-link').string
            bookURL = "https://www.casadellibro.com" + book.find('a', class_='title-link')['href']
            author = book.find('div', class_='mod-libros-author').text
            imageURL = book.find('img', class_='img-shadow')['data-src']
            f = urllib.request.urlopen(bookURL)
            html2 = f.read()
            f.close()
            detailssoup = BeautifulSoup(html2, 'lxml')
            details = detailssoup.find('div', class_='book-description')
            bookdata = details.find('ul', class_='list07')
            detailsli = bookdata.find_all('li')
            npages = 0
            editorial = ""
            lengua = ""
            encuadernacion = ""
            for detail in detailsli:
                if (detail.text[0:15] == "Nº de páginas: "):
                    npages = int(detail.text[15:18])
                if (detail.text[0:11] == "Editorial: "):
                    editorial = detail.text[11:]
                if (detail.text[0:8] == "Lengua: "):
                    lengua = detail.text[8:]
                if (detail.text[0:16] == "Encuadernación: "):
                    encuadernacion = detail.text[16:]
            if (details.find('div', class_='col02') != None):
                resumen = details.find('div', class_='col02').find('p')
            binding = ""
            if(encuadernacion == "Tapa dura"):
                binding = "D"
            elif(encuadernacion == "Tapa blanda"):
                binding = "B"
            synopsis = ""
            if(resumen != None):
                synopsis = resumen.text
            print(title)
            Book.objects.create(title=title, bookURL=bookURL, author=author, coverURL=imageURL, npages=npages,
                            editorial=editorial, language=lengua, category="Contemporánea", binding=binding, synopsis=synopsis)

