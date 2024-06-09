from rest_framework import serializers
from .models import Friendship, User, UserProfile
from django.contrib.auth.hashers import make_password
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user =  User.objects.filter(email = data['email'])
        if  user.exists():
            user = user.first()
            if user.check_password(data['password']):
                return user 
        raise serializers.ValidationError("Invalid Username / Password")
        

class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ('email','password')
    def validate(self, attrs):
        user =  User.objects.filter(email = attrs['email'])
        if  user.exists():
            raise serializers.ValidationError("Already an Account exists with this email.")
        attrs['password']  = make_password(attrs['password'])
        return attrs

