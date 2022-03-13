from rest_framework import serializers
from .models import Book,Log,Department,Facultie,SubjectCode, User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class FacultiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultie
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SubjectCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCode
        fields= '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['username','phone','email','university_id','first_name','last_name','password']
        read_only_fields = ['last_login',]
    
    extra_kwargs = {
        'email':{'required':False}
    }



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','phone','last_login','password']
    
    # extra_kwargs = {
    #     'password':{'HiddenField ':True}
    # }



