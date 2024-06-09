from django.urls import path

from connections.views import  AcceptedFriendRequestsView, FriendRequestDeclineView,  ProfileListView, ReceivedFriendRequestsView,FriendRequestSendView,FriendRequestAcceptView,FriendsListView


urlpatterns = [
    path('find_friends',ProfileListView.as_view()),
    
    path('accepted_requests',AcceptedFriendRequestsView.as_view()),
    path('received_requests',ReceivedFriendRequestsView.as_view()),

    path('send_friend_request',FriendRequestSendView.as_view()),
    path('accept_friend_request',FriendRequestAcceptView.as_view()),
    path('decline_friend_request',FriendRequestDeclineView.as_view()),

    path('friends',FriendsListView.as_view())
]