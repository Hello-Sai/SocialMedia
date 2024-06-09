from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, UserProfile

from accounts.serializers import AccountSerializer, UserSerializer
class SignUpView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = AccountSerializer



class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    def post(self,request):
        email =request.data.get('email')
        username = email.split("@")[0]
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():# user = User.objects.get(username = username)
            user = serializer.validated_data
            token = RefreshToken.for_user(user = user)
            return Response({'access':str(token.access_token),'refresh':str(token)})
        return Response(serializer.errors)


        
class LogoutView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self,request):

        request.META.pop('HTTP_AUTHORIZATION')
        response = Response({'message':"You have Logged Out Successfully"},200)
        response.set_cookie('HTTP_AUTHORIZATION',None)
        return response
    
