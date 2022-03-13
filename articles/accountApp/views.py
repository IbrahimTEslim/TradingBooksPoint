import email
from django.shortcuts import render

from .serializer import ChangePasswordSerializer,UserConfirmationSerializer
from django.contrib.auth import get_user_model


from rest_framework import status
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView

from rest_framework.authtoken.models import Token

from django.contrib.auth.tokens import default_token_generator

import hashlib
import itertools
import secrets

from django.core.mail import send_mail
from django.urls import reverse

from .models import ConfirmationToken

# Create your views here.
class ChangePasswordView(GenericAPIView, UpdateModelMixin):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = get_user_model()

    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ConfirmationEmail(GenericAPIView):

    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        res = secrets.token_hex(32)
        ConfirmationToken.objects.update_or_create(user=request.user,defaults={'token':res})

        
        send_mail(
            "Trading Books Point - Email Confirmation",
            "{}?token={}".format(reverse('user_confirmation'), res),
            "tradingbookspoint@gmail.com",
            [request.user.email]
        )

        return Response({'token':res,'message':'confirmation email sent'})

        

class ConfirmUser(GenericAPIView,UpdateModelMixin):
    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    serializer_class = UserConfirmationSerializer


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        if not serializer.is_valid():
            print("\nErrors: ",serializer.errors,"\n")
            return Response({'message':'Not Valid Data','error':serializer.errors})
        if request.user is None: return Response({'message':'No User Provided!'})
        if request.data['token'] is None: return Response({'message':'No Token Provided!'})
        user = request.user
        token = request.data['token']
        try:
            recorded_token = ConfirmationToken.objects.get(token=token)
        except(ConfirmationEmail.DoesNotExist,OverflowError,TypeError):
            return Response({'message':'Unrecorded Token!'})
        if recorded_token.user.id != user.id: return Response({'message':'How can that even happen (O_O) !!!'})
        user.is_confirmed = True
        user.save()

        recorded_token.delete()

        return Response({'status':'OK','message':'Confirmed'})









