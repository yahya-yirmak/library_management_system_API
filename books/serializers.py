from rest_framework import serializers
from .models import Author, Book


# Create a Serializer for Author Model
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio']


# Create a Serializer for Book Model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'number_of_copies_available']

    def validate_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError('This book already exists.')
        return value