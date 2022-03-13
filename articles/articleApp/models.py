from enum import unique
from typing import Optional
from django.core.exceptions import FieldError
from random import choices
from re import A, S
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.hashers import make_password

# from django.contrib.auth.forms import AdminPasswordChangeForm

from rest_framework.response import Response
from rest_framework import status

from django.apps import apps

from .validators import validate_university_id

from django.db.models import When, Case, Sum, IntegerField

# Create your models here.

class User(AbstractUser):
    user_role = (
        (1,'Admin'),
        (2,'Normal Client'),
    )

    # password = models.CharField(null = False, blank = False, max_length=120)
    phone = PhoneNumberField(unique=True,blank=True,null=True)
    email = models.EmailField(unique = True,blank=True,null=True)
    rule = models.IntegerField(choices=user_role, default=2)
    is_confirmed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    university_id = models.CharField(max_length=10,validators=[validate_university_id],blank=False,null=False,unique=True)

    # change_password_form = AdminPasswordChangeForm
    
    
    # def save(self,*args,**kwargs):
    #     # print("\nDict Data: ",kwargs,"\n")
    #     # print("\nargs Data: ",args,"\n")
    #     # print("\nargs Data 1st: ",args[0],"\n")
    #     # print("\nargs Data 2es: ",args[1],"\n")
    #     if not 'no_hash_pass' in kwargs or kwargs.pop('no_hash_pass') is False:
    #         print("Yeaaaaaah it worked !!")
    #         print("\n model pass before: ",self.password,"\n")
    #         self.set_password(self.password)
    #         print("\n model pass after: ",self.password,"\n")
    #     super(User,self).save(*args,**kwargs)


    def __str__(self): return self.first_name + " " + self.last_name


class Department(models.Model):
    name = models.CharField(max_length=50,unique=True)
    facultie = models.ForeignKey("Facultie",on_delete=models.DO_NOTHING)

    def __str__(self): return self.name


class Facultie(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self): return self.name


class SubjectCode(models.Model):

    semesters = (
        (1,"First Semester"),
        (2,"Seconod Semester")
        )

    subject_id = models.CharField(primary_key=True,max_length=10,unique=True)
    name = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    is_universirty_requirement = models.BooleanField(default=False)
    semester = models.IntegerField(choices = semesters)
    def __str__(self): return self.subject_id


class Book(models.Model):
    name = models.CharField(max_length=50)
    subject_code = models.ForeignKey(SubjectCode,on_delete=models.DO_NOTHING)
    author_name = models.CharField(max_length=50)

    @staticmethod
    def get_amount(book_id)->int:

        """
            calculate the amount from Log table
        """
        all_log = Log.objects.filter(book = book_id)
        totals = all_log.aggregate(
            donate = Sum(Case(When(op_code=1, then='amount'))),
            give_back = Sum(Case(When(op_code=2, then='amount'))),
            borrow = Sum(Case(When(op_code=3, then='amount'))),
            reserved = Sum(Case(When(op_code=4, then='amount'))),
        )

        donate = int(totals['donate'] or 0)
        give_back = int(totals['give_back'] or 0)
        borrow = int(totals['borrow'] or 0)
        reserved = int(totals['reserved'] or 0)

        print("\nList:",totals,"\n")
        # print("\nList:",b,"\n")
        return donate + give_back - borrow - reserved #if amount else 0


    def __str__(self): return self.name


class Log(models.Model):

    op_codes = (
        (1,'Donate'),
        (2,'GiveBack'),
        (3,'Borrow'),
        (4,'Reserved'),
    )

    op_codes_numbers = (1,2,3,4)

    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='cleint')
    book = models.ForeignKey(Book,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=1)
    op_code = models.IntegerField(choices = op_codes)
    confirmed_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='admins')



