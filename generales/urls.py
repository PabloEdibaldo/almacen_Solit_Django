from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'Usuario', views.UserProfile_ViewSet,'Usuario')

urlpatterns = [
    path('', include(router.urls)),
]
