from django.urls import path,include

from accounts.views import LoginView, LogoutView, SignUpView

urlpatterns =[
    path('signup',SignUpView.as_view()),
    path('login',LoginView.as_view()),
    path('logout',LogoutView.as_view())
]