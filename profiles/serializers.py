from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.authtoken.models import Token
from django.db import transaction

class SignUpSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    website_url = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(
        required=False, 
        allow_blank=True, 
        min_length=50,
        trim_whitespace=True
    )
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token', 'website_url', 'bio']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(
            user=user,
            website_url=validated_data.get('website_url', ''),
            bio=validated_data.get('bio', '')
        )
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
    user = UserSerializer()
    
    website_url = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(
        required=False, 
        allow_blank=True, 
        min_length=50,
        trim_whitespace=True
    )
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'website_url', 'user']
    
    def validate(self, attrs):
        user_data = attrs.get('user', {})
        email = user_data.get('email')
        username = user_data.get('username')

        if username and User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError({"user": {"username": "This username is already in use."}})

        if email and User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError({"user": {"email": "This email is already in use."}})
        
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context['request'].user
        user_data = validated_data.pop('user', {})

        # Update UserProfile fields
        instance.bio = validated_data.get('bio', instance.bio)
        instance.website_url = validated_data.get('website_url', instance.website_url)
        instance.save()

        # Update User fields if provided
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()
        
        return instance