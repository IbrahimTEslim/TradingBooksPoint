from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from articleApp.models import User

class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print("\nHead Of MEthod\n")
        try:
            user = get_user_model().objects.get(username=username)
            # print("\nFetched the User\n")
            if user.check_password(password) and user.is_active: return user
            else: return None
        except User.DoesNotExist:
            # print("\nUser Does Not Exist\n")
            return None

    def get_user(self,user_id):
        try:
            # print("Head Of get_user\n")
            return get_user_model().objects.get(id=user_id)
        except User.DoesNotExist:
            # print("\nget_user Does Not Exist\n")
            return None