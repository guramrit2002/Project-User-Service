from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectAccountViewSet

router = DefaultRouter()

router.register(r'', ProjectAccountViewSet, basename='project')
urlpatterns = router.urls
