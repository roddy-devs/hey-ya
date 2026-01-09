from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, HoleViewSet

router = DefaultRouter()
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'holes', HoleViewSet, basename='hole')

urlpatterns = [
    path('', include(router.urls)),
]
