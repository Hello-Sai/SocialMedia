from rest_framework import serializers
from accounts.models import UserProfile,Friendship


class FriendSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.user.email



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user',)
    def to_representation(self, instance):
        return str(instance.user.username)

class SendRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    username = serializers.CharField(source="user.username",write_only=True)
    class Meta:
        model = UserProfile
        fields = [ 'user','username']
    def to_representation(self, instance):
        return instance.user.username




class ReceivedFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('from_user',)
    def to_representation(self, instance):
        return instance.from_user.user.username



class FriendsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='to_user.user.email')

    class Meta:
        model = Friendship
        fields = ('email', 'is_accepted', 'created_at')

class UserProfileSerializer(serializers.ModelSerializer):
    profiles = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('profiles',)
    def get_profiles(self,obj):
        return FriendSerializer(UserProfile.objects.exclude(id= obj.id),many=True).data
    

class FriendRequestAcceptSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()
    class Meta:
        model = Friendship
        fields = ('to_user',)

