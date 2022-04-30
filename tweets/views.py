import json
import random
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

ALLOWED_HOST =  settings.ALLOWED_HOSTS
# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST'])
## @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(["GET"])
def tweet_detail_view(reqest, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializers = TweetSerializer(obj)
    return Response(serializers.data, status=200)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(reqest, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=reqest.user)
    if not qs.exists():
        return Response({"message":"You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet removed"}, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_action_view(reqest, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=reqest.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")

        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(reqest.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(reqest.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(user=reqest.user, parent=obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

@api_view(["GET"])
def tweet_list_view(reqest, *args, **kwargs):
    qs = Tweet.objects.all()
    serializers = TweetSerializer(qs, many=True)
    return Response(serializers.data)

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOST):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view_pure_django(reqest, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request,tweet_id, *args, **kwargs):
    """
    REST API VIEW
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status1 = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status1 = 404

    return JsonResponse(data, status=status1)