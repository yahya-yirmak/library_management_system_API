from rest_framework import serializers
from .models import CheckOut
from books.models import Book
from django.utils.timezone import now


# Create a Serializer for CheckOut Model
class CheckOutSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CheckOut
        fields = ['id', 'member', 'book', 'check_out_date', 'return_date', 'status']
    

    def validate(self, data):
        """
            Checks if the book has available copies and if the member has already checked out the book.
            Raises a validation error if no copies are available or if the member has already checked out the book.
        """
        book = data['book']
        member = data['member']
        
        if book.number_of_copies_available == 0:
            raise serializers.ValidationError('No copies available at the moment.')
        
        if CheckOut.objects.filter(book=book, member=member, status='checked_out'):
            raise serializers.ValidationError('You have already checked out this book.')

        return data
    
    
    def create(self, validated_data):
        """
            Creates a new checkout record and updates the book's available copies.
        """
        book = validated_data['book']
        book.number_of_copies_available -= 1
        book.save()

        return super().create(validated_data)