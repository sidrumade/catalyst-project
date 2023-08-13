from django.urls import path
from django.views.decorators.http import require_POST

from .views import UserProfileView , BaseView , upload_csv # Replace with your actual view

app_name = 'catalyst'

urlpatterns = [
    path('', BaseView.as_view() , name='home'),
    path('upload/', require_POST(upload_csv) , name='upload'),
    path('accounts/login/user/profile', UserProfileView.as_view(), name='user_profile'),

]
