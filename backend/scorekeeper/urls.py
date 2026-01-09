from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, HoleViewSet
from .auth_views import login_view, logout_view

router = DefaultRouter()
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'holes', HoleViewSet, basename='hole')

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('', include(router.urls)),
]
