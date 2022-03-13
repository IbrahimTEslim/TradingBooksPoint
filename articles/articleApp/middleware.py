from urllib.parse import parse_qs
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
import jwt
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from jwt import decode as jwt_decode
from django.conf import settings

class TokenVerifyMiddleware:
    def __init__(self,get_response) -> None:
        self.get_response = get_response

    def __call__(self,request):
        close_old_connections()

        if request.path.split('/')[1] == 'account': return None

        print("\n\npath: ",request.path.split('/'),"\n\n")

        token = request.META['HTTP_AUTHORIZATION'].split()[1]

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return JsonResponse({'message':'InvalidToken'})
        else:
            decoded_data = jwt_decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            request.user = get_user_model().objects.get(pk=decoded_data['user_id'])
        return self.get_response(request)

    
