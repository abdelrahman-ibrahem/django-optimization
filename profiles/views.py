from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer, SignUpSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated



class UserProfileViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_action_map = {
            'signup': SignUpSerializer,
            'login': LoginSerializer,
        }
        return serializer_action_map.get(self.action, super().get_serializer_class())

    @action(detail=False, methods=['post'], permission_classes=[])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_data = serializer.save()
        return Response(user_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_data = serializer.save()
        return Response(user_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user.userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @me.mapping.patch
    def update_me(self, request):
        user = request.user
        serializer = self.get_serializer(user.userprofile, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    