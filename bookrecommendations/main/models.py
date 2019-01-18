from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    bookURL = models.URLField()
    author = models.CharField(max_length=50)
    coverURL = models.URLField()
    npages = models.IntegerField()
    editorial = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    binding = models.CharField(max_length=50, choices=(('B', 'Tapa blanda'),('D','Tapa dura'),))
    category = models.CharField(max_length=50, choices=(('Contemporánea', 'Contemporánea'),('Negra', 'Negra')))
    synopsis = models.TextField(null=True)

    def __str__(self):
        return self.title


