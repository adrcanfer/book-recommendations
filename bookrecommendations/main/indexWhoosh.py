import os
from whoosh.index import create_in,open_dir
from whoosh.fields import ID, TEXT, KEYWORD, Schema
from whoosh.qparser import MultifieldParser

from main.models import Book

def createSchema():
    booksSchema = Schema(id=ID(stored=True), title=TEXT, author=KEYWORD,
                         editorial=ID, synopsis=TEXT)
    if not os.path.exists("booksIndex"):
        os.mkdir("booksIndex")
        create_in("booksIndex", schema=booksSchema)

def indexBooks():
    books = Book.objects.all()
    ix = open_dir("booksIndex")
    writer = ix.writer()
    for b in books:
        writer.add_document(id=str(b.id), title=b.title, author=b.author,
                            synopsis=b.synopsis)
    writer.commit()
