
from multiprocessing import context
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ..models import Profile
from ..serializers import PublicProfileSerializer


User = get_user_model()
ALLOWED_HOST =  settings.ALLOWED_HOSTS
# Create your views here.
@api_view(['GET', 'POST'])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        me = request.user
        action = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
            else:
                pass
    serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def user_follow_view(request, username, *args, **kwargs):
#     me = request.user
#     other_user_qs = User.objects.filter(username=username)
#     if me.username == username:
#         my_followers = me.profile.followers.all()
#         return Response({"count": my_followers.count()}, status=200)
#     if not other_user_qs.exists():
#         return Response({}, status=404)
#     other = other_user_qs.first()
#     profile = other.profile
#     data = request.data or {}
#     action = data.get("action")
#     if action == "follow":
#         profile.followers.add(me)
#     elif action == "unfollow":
#         profile.followers.remove(me)
#     else:
#         pass
#     data = PublicProfileSerializer(instance=profile, context={"request": request})
#     return Response(data.data, status=200)
