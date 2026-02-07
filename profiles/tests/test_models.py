import pytest
from profiles.models import UserProfile

pytestmark = pytest.mark.django_db

class TestUserProfileModel:
    def test_user_profile_creation(self, test_user):
        profile = UserProfile.objects.create(user=test_user, bio="This is a test bio.")
        assert profile.user.username == "testuser"
        assert str(profile) == "testuser"