from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Friendship, User, UserProfile
from rest_framework.generics import CreateAPIView,GenericAPIView,ListAPIView
from connections.serializers import  FriendRequestAcceptSerializer, ProfileSerializer, ReceivedFriendSerializer, SendRequestSerializer
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from connections.paginations import CustomPagination
from rest_framework.throttling import UserRateThrottle
class FriendsListView(ListAPIView):
    serializer_class = ProfileSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        user_profile = self.request.user.profile

        return user_profile.friends.all()

class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        user_profile = self.request.user.profile
        search = self.request.query_params.get('search')
        queryset = UserProfile.objects.exclude(id=user_profile.id)
        if search:
            print(search)
            return queryset.filter(user__email__icontains = search)
        return queryset

class AcceptedFriendRequestsView(ListAPIView):
    serializer_class = ReceivedFriendSerializer
    
    def get_queryset(self):
        return Friendship.objects.filter(to_user = self.request.user.profile,is_accepted=True )
    
    
class ReceivedFriendRequestsView(ListAPIView):
    serializer_class = ReceivedFriendSerializer
    def get_queryset(self):
        received_friend_requests = Friendship.objects.filter(to_user = self.request.user.profile)
        return received_friend_requests


    
class FriendRequestSendView(GenericAPIView):
    serializer_class = SendRequestSerializer
    throttle_classes =[UserRateThrottle]
    def get_queryset(self):
        user_profile = self.request.user.profile
        # sent_requests = Friendship.objects.filter(from_user=user_profile).values_list('to_user', flat=True)
        # received_requests = Friendship.objects.filter(to_user=user_profile).values_list('from_user', flat=True)
        # print('sent are ',sent_requests)
        # print('received are ',received_requests)

        # print('send are ',user_profile.from_user.all().values_list('to_user',flat=True))
        # print('receivedd are ',user_profile.to_user.all().values_list('from_user',flat=True))
        # Combine the sent and received request user ids
        # excluded_ids = list(sent_requests) + list(received_requests)
        excluded_ids = list(user_profile.friends.all().values_list('id',flat=True))
        print(excluded_ids)
        # Exclude the current user and those with existing friendship requests
        queryset = UserProfile.objects.exclude(id__in=excluded_ids).exclude(id=user_profile.id)
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username') or request.data.get('email').split('@')[0]
        profile = UserProfile.objects.filter(user__username=username).first()
        if not profile:
            return Response({"error": "Profile Not Exists"}, status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.get_or_create(from_user=request.user.profile, to_user=profile)
        return Response({'success': True, 'message': 'Successfully request Sent'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors)
            
    

class FriendRequestAcceptView(APIView):
    serializer_class = FriendRequestAcceptSerializer
    
    
    def post(self,request):
        print(request.data,request.data.get('username'))
        username = request.data.get('username') or request.data.get('email').split('@')[0]
        profile = UserProfile.objects.filter(user__username = username)
        if not profile.exists():
            return Response({'success':False,'error':"Profile doesn't exists."},status=400)
        obj = Friendship.objects.filter(from_user = profile.first(),to_user = request.user.profile)
        if obj.exists() :
            obj.update(is_accepted = True)
            Friendship.objects.get_or_create(to_user = profile.first(),from_user = request.user.profile)
            return Response({'success':True,'message':'Friend Request Accepted'})
        return Response({'success':False,'error':'Friend Request not found'},status=400)
    

class FriendRequestDeclineView(APIView):
    serializer_class = FriendRequestAcceptSerializer
    def get_queryset(self):
        user_profile = self.request.user.profile
        return UserProfile.objects.exclude(user_profile)
    
    def post(self,request):
        username = request.data.get('username')or request.data.get('email').split('@')[0]
        profile = UserProfile.objects.filter(user__username = username)
        if not profile.exists():
            return Response({'success':False,'error':"Profile doesn't exists."},status=400)
        obj = Friendship.objects.filter(from_user = profile.first(),to_user = request.user.profile)
        if obj.exists() :
            obj.delete()    
            return Response({'success':True,'message':'UnFriend Done Successfully'})
        return Response({'success':False,'error':'Friend Request not found'},status=400)