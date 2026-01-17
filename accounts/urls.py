from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    *router.urls
]
