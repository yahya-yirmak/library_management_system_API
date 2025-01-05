from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckOutViewSet

router = DefaultRouter()
router.register(r"checkouts", CheckOutViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
