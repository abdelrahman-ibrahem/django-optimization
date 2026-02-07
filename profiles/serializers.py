from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.authtoken.models import Token
from django.db import transaction

class SignUpSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        token = Token.objects.create(user=user)
        user.token = token.key
        return {
            'username': user.username,
            'email': user.email,
            'token': str(token.key)
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        self.user = user
        return attrs

    def create(self, validated_data):
        token, created = Token.objects.get_or_create(user=self.user)
        return {
            'username': self.user.username,
            'email': self.user.email,
            'token': str(token.key)
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']



class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    website_url = serializers.URLField(required=False, allow_blank=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'website_url', 'user']

    def validate_bio(self, value):
        if value and len(value.strip()) < 50:
            raise serializers.ValidationError("The bio must be at least 50 characters long.")
        return value

    def update(self, instance, validated_data):
        with transaction.atomic():
            # Update UserProfile fields
            instance.bio = validated_data.get('bio', instance.bio)
            instance.website_url = validated_data.get('website_url', instance.website_url)
            instance.save()
        
        instance.refresh_from_db()  # Refresh instance to get updated data
        return instance