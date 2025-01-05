
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status



# Create a view for handling CRUD operations for Library users
class CustomUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True)


# Create a View for Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'message': 'The user has been logged in successfully.', 'token': token.key},
            status=status.HTTP_200_OK
        )


# Create a View For Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'message':'User has been successfully created'},
                status=status.HTTP_201_CREATED
            )
        