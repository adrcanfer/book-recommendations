from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    bookURL = models.URLField()
    author = models.CharField(max_length=100)
    npages = models.IntegerField()
    editorial = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    coverURL = models.URLField()
    binding = models.CharField(max_length=100, choices=(('Tapa blanda', 'Tapa blanda'), ('Tapa dura', 'Tapa dura'),))
    category = models.CharField(max_length=100, choices=(
        ('Contemporánea', 'Contemporánea'), ('Negra', 'Negra'), ('Romántica', 'Romántica'), ('Cómics', 'Cómics'),
        ('Historia', 'Historia') ,('Adolescentes', 'Adolescentes'), ('Infantil', 'Infantil')))
    synopsis = models.TextField(max_length=3000, null=True)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=50, unique=True, error_messages={'unique':"El nombre de usuario ya existe"})
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username + " - " + str(self.id)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return str(self.id) + " - " + str(self.rating)
