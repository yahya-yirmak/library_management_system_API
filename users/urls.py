from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, LoginView, RegisterView

router =DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
]