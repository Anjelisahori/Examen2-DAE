from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LetraCancionViewSet

router = DefaultRouter()
router.register(r'letras', LetraCancionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
