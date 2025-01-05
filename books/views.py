from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):
    """
        A viewset for CRUD operations on Author objects.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer



class BookViewSet(viewsets.ModelViewSet):
    """
        A viewset for CRUD operations on Book objects.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly] # Unsafe methods only for admins.

    queryset = Book.objects.all()
    serializer_class = BookSerializer


    def get_queryset(self):
        """
            Admins can see all books, but members can see only available books.
        """
        user = self.request.user
        if user.is_staff:
            return Book.objects.all()
        
        return Book.objects.filter(number_of_copies_available__gt=0)
