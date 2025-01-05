from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CheckOut
from .serializers import CheckOutSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .permissions import DeleteForAdminOnly
# Create your views here.


class CheckOutViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on CheckOut objects. 
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = CheckOut.objects.all()
    serializer_class = CheckOutSerializer

    def get_queryset(self):
        return CheckOut.objects.filter(member=self.request.user)
    


    @action(detail=True, methods=["patch"], url_path="return")
    def return_book(self, request, pk=None):
        """
            Handles the return of a book by a member.
            Updates the book's available copies and marks the checkout as returned.
            Returns an error if the book has already been returned or if the checkout ID is invalid.
            Responds with a success message if the book is successfully returned.
        """
        try:
            checkout = self.get_object()
            if checkout.status == 'returned':
                return Response({'error':'You already returned this book'}, status=status.HTTP_400_BAD_REQUEST)
            
            book = checkout.book
            book.number_of_copies_available += 1
            book.save()

            checkout.status = 'returned'
            checkout.return_date = now()
            checkout.save()
            return Response({'message':'The book has been successfully returned'}, status=status.HTTP_200_OK)
        
        except CheckOut.DoesNotExist:
            return Response({'error':'Invalid checkout ID'}, status=status.HTTP_400_BAD_REQUEST)

        

    