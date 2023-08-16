from django.urls import path
from django.views.decorators.http import require_POST

from .views import UserProfileView , BaseView , upload_csv , get_log_status , search_records # Replace with your actual view

app_name = 'catalyst'

urlpatterns = [
    path('', BaseView.as_view() , name='home'),
    path('upload/', require_POST(upload_csv) , name='upload'),
    path('accounts/login/user/profile', UserProfileView.as_view(), name='user_profile'),
    path('logs/json/', get_log_status , name='logs-json'),
    path('search/', search_records, name='search_records'),



]
