from django.urls import path

from .views import get_book_quantity
from.views import BookMixins, LogListMethods,UserMixins,LogMixins,FacultyMixins,DepartmentMixins,SubjectCodeMixins,ProfileMethods

from rest_framework.authtoken import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path('book/',BookAPI.as_view(),name='APIBook'),
    path('mixb/',BookMixins.as_view(),name='mixBook'),
    path('mixb/<int:id>/',BookMixins.as_view(),name='mixBook'),
    
    path('mixu/',UserMixins.as_view(),name='mixBook'),
    path('mixu/<int:id>/',UserMixins.as_view(),name='mixBook'),

    path('mixl/',LogMixins.as_view(),name='mixBook'),
    path('mixl/<int:id>/',LogMixins.as_view(),name='mixBook'),

    path('mixf/',FacultyMixins.as_view(),name='mixBook'),
    path('mixf/<int:id>/',FacultyMixins.as_view(),name='mixBook'),

    path('mixd/',DepartmentMixins.as_view(),name='mixBook'),
    path('mixd/<int:id>/',DepartmentMixins.as_view(),name='mixBook'),

    path('mixs/',SubjectCodeMixins.as_view(),name='mixBook'),
    path('mixs/<int:id>/',SubjectCodeMixins.as_view(),name='mixBook'),

    path('login/',views.obtain_auth_token),



    path('getlog/<code>/',LogListMethods.as_view()),

    path('getuser/<id>/',ProfileMethods.as_view(),name='profileEndPoint'),

    path('getBookQuantity/<book_id>/',get_book_quantity,name='getBookAmount'),

]