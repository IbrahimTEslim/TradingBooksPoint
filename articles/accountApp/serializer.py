from rest_framework import  serializers
from django.contrib.auth import get_user_model

from .models import ConfirmationToken

import datetime

# from articleApp.models import User


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):

    registeration_optional_fields = ('first_name','last_name','email','phone')

    def validate(self,data):
        # print("\nRegister Validation Run !!\n\n")
        if 'email' not in data and 'phone' not in data:
             raise serializers.ValidationError({'email':"Not allowed to let Email & Phone Both be Null values!"})

        if (data['email'] is None or len(data['email']) <= 1) and (data['phone'] is None or len(data['phone']) <= 1):
             raise serializers.ValidationError({'email':"Not allowed to let Email & Phone Both be Null values!"})
        # print("\nValidation Okay\n")
        return data

    class Meta:
        model = get_user_model()
        
        fields = ('username','password','first_name', 'last_name','university_id','phone','email',)
        # extra_kwargs = {
        #     'password':{'write_only': True},
        #     'username':{
        #         'error_messages':{
        #             'required': 'Give Yourself a username',
        #             'unique':'This Username Already Used'
        #         }
        #     }
        # }
    def create(self, validated_data):
        for field in self.registeration_optional_fields:
            if field not in validated_data:
                validated_data[field] = None
        print("\nData: ",validated_data,"\n")
        user = get_user_model()(username = validated_data['username'],
                            first_name = validated_data['first_name'] or '', last_name = validated_data['last_name'] or '',
                            university_id = validated_data['university_id'], email = validated_data['email'] or '',
                            phone = validated_data['phone'] or '', is_admin = False, is_staff = False, is_active = True,
                            is_superuser = False, is_confirmed = False, last_login = datetime.datetime.now(), rule = 2)
        print("\n\nPAssword: ",validated_data['password'],"\n")
        user.set_password(validated_data['password'])
        user.save()
        return user




class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['old_password','new_password']

class EmailConfirmationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfirmationToken
        fields = '__all__'


class UserConfirmationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'