from django.urls import path , include
from django.views.decorators.http import require_POST

from .views import BaseView , upload_csv , get_log_status , search_records  # Replace with your actual view

from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet,CompanyCountAPIView,UserListView,delete_user,add_user

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

app_name = 'catalyst'

urlpatterns = [
    path('', BaseView.as_view() , name='home'),
    path('upload/', require_POST(upload_csv) , name='upload'),
    # path('accounts/login/user/profile', UserProfileView.as_view(), name='user_profile'),
    path('logs/json/', get_log_status , name='logs-json'),
    path('search/', search_records, name='search_records'),
    path('api/companies/count/', CompanyCountAPIView.as_view(), name='count-companies'),
    path('rest-api/', include(router.urls)),
    path('list-user/', UserListView.as_view(), name='list-user'),
    path('delete/<int:pk>/', delete_user, name='delete-user'),  # Add this line
    path('add-user/', add_user, name='add-user'),

]


