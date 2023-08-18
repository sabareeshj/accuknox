from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name = 'signup'),
    path('login', views.login, name = 'login'),
    path('user-search', views.user_search, name='user-search'),
    path('friend-request/', views.friend_request_action, name='friend-request-action'),
    path('list-friends/', views.list_friends, name='list-friends'),
]