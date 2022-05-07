from django.urls import path

from .views import (
    user_follow_view
)
'''
Base ENDPOINT /api/profiles/
'''
urlpatterns = [
    path('<str:username>/follow', user_follow_view),
]
