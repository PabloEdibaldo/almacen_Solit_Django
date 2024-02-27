from rest_framework import viewsets

from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfile_ViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()