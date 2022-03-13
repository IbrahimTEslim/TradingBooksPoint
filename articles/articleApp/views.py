
from ast import Return
from urllib import response
from .models import Log,Book,Facultie,Department,SubjectCode,User
from .serializers import LogSerializer,BookSerializer,FacultiesSerializer,DepartmentSerializer, ProfileSerializer,SubjectCodeSerializer, UserSerializer

from rest_framework.mixins import RetrieveModelMixin,ListModelMixin,UpdateModelMixin,CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

from rest_framework.response import Response

from django.contrib.auth.hashers import make_password

from .my_pagination import LogPagination, BooksPagination

from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter

from .my_filters import LogFilter

from rest_framework import status
from rest_framework.decorators import api_view

from .my_permissions import IsConfirmed

class BookMixins(GenericAPIView,RetrieveModelMixin,ListModelMixin,CreateModelMixin,UpdateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    lookup_field = 'id'


    pagination_class = BooksPagination

    # filter_class = LogFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


    def get(self,request,id=None):
        if id: return self.retrieve(request,id)
        else: return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,id):
        return self.update(request,id)



class FacultyMixins(GenericAPIView,RetrieveModelMixin,ListModelMixin,CreateModelMixin,UpdateModelMixin):
    serializer_class = FacultiesSerializer
    queryset = Facultie.objects.all()

    permission_classes = [IsAdminUser]


    lookup_field = 'id'

    def get(self,request,id=None):
        if id: return self.retrieve(request,id)
        else: return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,id):
        return self.update(request,id)



class DepartmentMixins(GenericAPIView,RetrieveModelMixin,ListModelMixin,CreateModelMixin,UpdateModelMixin):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    permission_classes = [IsAdminUser]

    lookup_field = 'id'

    def get(self,request,id=None):
        if id: return self.retrieve(request,id)
        else: return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,id):
        return self.update(request,id)



class LogMixins(GenericAPIView,RetrieveModelMixin,ListModelMixin,CreateModelMixin,UpdateModelMixin):
    serializer_class = LogSerializer
    queryset = Log.objects.all()

    
    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated,IsConfirmed]

    lookup_field = 'id'

    pagination_class = LogPagination

    # filter_class = LogFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    # search_fields = ['amount','user','book']

    def get(self,request,id=None):
        print("user: ",request.user.pk)
        print("auth: ",request.auth)
        # if request.user is None: self.queryset = None
        if id: return self.retrieve(request,id)
        else: return self.list(request)

    def post(self,request):
        print("\nData: ",request.data,"\n")

        serializer = self.get_serializer(data = request.data)

        if not serializer.is_valid(): return Response({'message':'Not Valid Data','errors':serializer.errors})

        wanted_amount = int(request.data['amount'])
        wanted_book = int(request.data['book'])

        amount_we_have = Book.get_amount(book_id=wanted_book)
        print("\nSome Detail: ",amount_we_have,"\n")
        print("\nwanted: ",wanted_amount,"\n")
        print("\nType have: ",type(amount_we_have),"\n")
        print("\nType want: ",type(wanted_amount),"\n")
        if amount_we_have <= 0:
            return Response({'message':'Sorry, this book is out of stock'})

        if amount_we_have < wanted_amount:
            return Response({'message':'Sorry, We don\'t have the amount you asked.'})

        return self.create(request)

    def put(self,request,id):
        return self.update(request,id)


class SubjectCodeMixins(GenericAPIView,RetrieveModelMixin,ListModelMixin,CreateModelMixin,UpdateModelMixin):
    serializer_class = SubjectCodeSerializer
    queryset = SubjectCode.objects.all()

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    lookup_field = 'id'

    def get(self,request,id=None):
        if id: return self.retrieve(request,id)
        else: return self.list(request)
    def post(self,request):
        return self.create(request)

    def put(self,request,id):
        return self.update(request,id)


class UserMixins(GenericAPIView,RetrieveModelMixin,UpdateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated,]

    lookup_field = 'id'

    def get(self,request,id=None):
        if id: return self.retrieve(request,id)
        else: return Response({'message':'missing User Id !'})

    def put(self,request,id):
        return self.update(request,id)



class LogListMethods(GenericAPIView, ListModelMixin):

    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated,IsConfirmed]

    lookup_field = 'id'

    serializer_class = LogSerializer
    queryset = Log.objects.all()

    pagination_class  = LogPagination

    def get(self,request,code):
        self.queryset = Log.objects.filter(user = request.user, op_code = code)
        # print('\code: ',code)
        # print("\ncodesss:: ",Log.op_codes_numbers)
        # if int(code) not in Log.op_codes_numbers: return Response({'message':'Invalid Operation Type'})
        # user = request.user
        # print('\nuser: ',user)
        # data = Log.objects.filter(user = user, op_code = code)
        # serializer = LogSerializer(data,many=True)
        # print('\ndata: ',data)
        # return Response(serializer.data)
        return self.list(request)


class ProfileMethods(GenericAPIView,RetrieveModelMixin,UpdateModelMixin):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated,]

    lookup_field = 'id'

    def get(self,request,id=None):
        print("\nId: ",request.user.id)
        print("\nData Id: ",id)
        if id: 
            if int(request.user.id) is int(id):
                return self.retrieve(request,id)
            else: 
                return Response({'message':'Not Your Profile'})
        else: 
            return Response({'message':'No User Id Provided'})

    def put(self,request,id):
        if id: 
            if int(request.user.id) is int(id):
                user = User.objects.get(pk=id)
                serializer = UserSerializer(user,data = request.data)
                serializer.is_valid()
                print("\nData: ",serializer.data,"\n")
                if serializer.is_valid():
                    
                    if user.email != serializer.data['email'] or user.phone != serializer.data['phone']:
                        #confirmation_here
                        return Response({'message':'adding confirmation here'})
                    else:
                        self.update(request,id)

                else: 
                    print("\nErrors: ",serializer.errors)
                    return Response({'message':'Invalid Data Given'})
                return Response()         
                
            else: 
                return Response({'message':'Not Your Profile'})
        else: 
            return Response({'message':'No User Id Provided'})
        


@api_view(['GET'])
def get_book_quantity(request,book_id):
    return Response({'value':Book.get_amount(book_id)})






# class ChangePasswordView(GenericAPIView, UpdateModelMixin):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     model = User

#     authentication_classes = [JWTAuthentication,SessionAuthentication,TokenAuthentication]
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class BookAPI(APIView):
#     def get(self,request):
#         articles = Book.objects.all()
#         serializer = BookSerializer(articles,many=True)
#         return Response(serializer.data)

#     def post(self,request):
#         serializer = BookSerializer(data = request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
