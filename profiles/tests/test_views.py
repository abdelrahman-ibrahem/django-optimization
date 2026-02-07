import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

class TestUserAuth:
    
    def test_signup_success(self, api_client):
        url = reverse('userprofile-signup')
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpassword123",
            "bio": "This is a sample bio that is definitely longer than fifty characters to pass validation.",
            "website_url": "https://example.com"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "token" in response.data
        assert response.data["username"] == "newuser"
    
    def test_signup_without_user_profile_data(self, api_client, test_user):
        url = reverse('userprofile-signup')
        data = {
            "username": "anotheruser",
            "email": "another@example.com",
            "password": "anotherstrongpassword123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "token" in response.data
        assert response.data["username"] == "anotheruser"

    def test_login_success(self, api_client, test_user):
        url = reverse('userprofile-login')
        data = {
            "email": test_user.email,
            "password": "password123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data

    def test_get_me_authenticated(self, auth_client, test_user):
        from profiles.models import UserProfile
        UserProfile.objects.get_or_create(user=test_user)
        
        url = reverse('userprofile-me')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['username'] == test_user.username

    def test_update_me_bio_validation(self, auth_client, test_user):
        from profiles.models import UserProfile
        UserProfile.objects.get_or_create(user=test_user)
        
        url = reverse('userprofile-me')
        data = {"bio": "Too short"} 
        response = auth_client.patch(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "bio" in response.data
        
        long_bio = "This is a very long bio that definitely exceeds the fifty character limit required by the serializer."
        response = auth_client.patch(url, {"bio": long_bio})
        assert response.status_code == status.HTTP_200_OK
    
    def test_update_me_website_url_validation(self, auth_client, test_user):
        from profiles.models import UserProfile
        UserProfile.objects.get_or_create(user=test_user)
        url = reverse('userprofile-me')
        data = {"website_url": "not-a-valid-url"}
        response = auth_client.patch(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "website_url" in response.data
        
        valid_url = "https://valid-url.com"
        response = auth_client.patch(url, {"website_url": valid_url})
        assert response.status_code == status.HTTP_200_OK
    
    def test_update_me_username_email(self, auth_client, test_user):
        from profiles.models import UserProfile
        UserProfile.objects.get_or_create(user=test_user)
        url = reverse('userprofile-me')
        new_username = "updateduser"
        new_email = "updated@example.com"

        response = auth_client.patch(
            url, 
            {"user": {"username": new_username, "email": new_email}}, 
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['username'] == new_username
        assert response.data['user']['email'] == new_email