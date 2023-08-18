from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.paginator import Paginator
from .models import FriendRequest, Friendship

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User(email=email, password=make_password(password))
    user.save()
    
    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)
    
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_search(request):
    keyword = request.query_params.get('keyword', '')

    if '@' in keyword:
        user = User.objects.filter(email=keyword).first()
        if(user):
            return Response({"user": user.email})
    else:
        users = User.object.filter(
            Q(username__icontains=keyword) |
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword)
        )
        paginator = Paginator(users, 10)
        page = request.query_parametes.get('page', 1)
        users_page = paginator.get_page(page)
        users_list = [{
            'username': user.username, 
            'email': user.email
        } for user in users_page]
        return Response({"users": users_list})
    
    return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes(['user'])
def friend_request_action(request):
    action = request.data.get('action')
    target_user_id = request.data.get('target_user_id')

    if action == 'send':
        return send_friend_request(request, target_user_id)
    elif action == 'accept':
        return accept_friend_request(request, target_user_id)
    elif action == 'reject':
        return reject_friend_request(request, target_user_id)
    else:
        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, target_user_id):
    try:
        target_user = User.objects.get(id=target_user_id)
    except User.DoesNotExist:
        return Response({"error": "Target user not found."}, status=status.HTTP_404_NOT_FOUND)

    if target_user == request.user:
        return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new friend request
    friend_request = FriendRequest(from_user=request.user, to_user=target_user, status='pending')
    friend_request.save()

    return Response({"message": f"Friend request sent to {target_user.username}."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, target_user_id):
    try:
        friend_request = FriendRequest.objects.get(from_user=target_user_id, to_user=request.user, status='pending')
    except FriendRequest.DoesNotExist:
        return Response({"error": "Pending friend request not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update the friend request status to 'accepted'
    friend_request.status = 'accepted'
    friend_request.save()

    # Create a mutual friendship entry
    Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)

    return Response({"message": "Friend request accepted and friendship created."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, target_user_id):
    try:
        friend_request = FriendRequest.objects.get(from_user=target_user_id, to_user=request.user, status='pending')
    except FriendRequest.DoesNotExist:
        return Response({"error": "Pending friend request not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update the friend request status to 'rejected'
    friend_request.status = 'rejected'
    friend_request.save()

    return Response({"message": "Friend request rejected."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    user = request.user
    friends = Friendship.objects.filter(user1=user)

    friends_list = [{"username": friend.user2.username, "email": friend.user2.email} for friend in friends]
    return Response({"friends": friends_list})



