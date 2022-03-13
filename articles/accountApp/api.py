from django.contrib.auth import get_user_model
from articleApp.models import User
from articleApp.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import generics, permissions, mixins
from .serializer import RegisterSerializer
from django.core.exceptions import FieldError
from rest_framework import status





class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        # print("\nRequest Data:",request.data,"\n\n")
        serializer = self.get_serializer(data = request.data)
        # print("\nSeri: ",serializer,"\n")
        if not serializer.is_valid():
            # print("\nErrors: ",serializer.error,"\n")
            return Response(
                {
                    'message':"Error or conflect in the given data, make sure you enter them correct.",
                    'error':serializer.errors
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        user = serializer.save()
        return Response ({
            'user':UserSerializer(user,context=self.get_serializer_context()).data,
            'message':"User Created Successfully. Now perform Login to get your token",
        })
