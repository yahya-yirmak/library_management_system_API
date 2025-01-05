from django.db import models


# CREATE AUTHOR MODEL
class Author(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    bio = models.TextField()

    def __str__(self):
        return f"{self.name}"


# CREATE A BOOK MODEL
class Book(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    isbn = models.CharField(max_length=18, unique=True)
    published_date = models.DateField()
    number_of_copies_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} by {self.author.name}"