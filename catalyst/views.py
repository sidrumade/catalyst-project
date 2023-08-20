from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.exceptions import ValidationError


from django.core.files.storage import FileSystemStorage

import pdb


from allauth.account.views import SignupView

from .tasks import process_file_upload
from django.shortcuts import redirect, get_object_or_404

from .models import UploadLog , Company
from django.http import JsonResponse
from .forms import CompanyModelForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CompanySerializer,CompanyCountSerializer,UserListSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailAddress


# Create your views here.



# class UserProfileView(LoginRequiredMixin):
#     template_name = 'account/user_profile.html'  # Path to your profile template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         context['user'] = user
#         return context




from .forms import CustomUserCreationForm

def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            # Redirect or display a success message
            return redirect('catalyst:list-user')  # Redirect to the user list after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/add_user.html', {'form': form})



class UserListView(ListView):
    model = User
    template_name = 'account/user_profile.html'
    context_object_name = 'users'
    
    

    
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
    return redirect('catalyst:list-user')


class UserHandlerView(TemplateView):
    template_name = 'account/user_profile.html'  # Path to your profile template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context
    
    
class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'account/base.html'  # Path to your profile template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context




def login_view(request):
    return render(request, 'account/login.html')



def upload_csv(request):
  """Handles the upload of a CSV file and inserts it into the database."""
  username = None
  if request.user.is_authenticated:
        username = request.user.username
        
        
  if request.method == 'POST':
    file = request.FILES['datafile']
    
    if not file:
        raise ValidationError("No file selected")
    
    # Specify the temporary folder path
    temp_folder = 'temp_uploads/'


    # Save the file to the filesystem
    fs = FileSystemStorage(location=temp_folder)
    filename = fs.save(file.name, file)
    
    if not filename.endswith('.csv'):
        raise ValidationError("Invalid file format. Please upload a CSV file.")
    
    
    if username:
        recept = process_file_upload.delay(temp_folder,filename,username)
        
    print('redirecting====================')
    return redirect('catalyst:home')
  else:
    return render(request, 'account/base.html')





def get_log_status(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        
        
    logs = UploadLog.objects.filter(user=username)
    
    logs_data = []
    for log in logs:
        logs_data.append({
            'id': log.id,
            'user': log.user,
            'file_name': log.file_name,
            'start_time' : log.start_time,
            'end_time': log.end_time ,
            'total_rows': log.total_rows,
            'process_rows': log.process_rows,
            'status' : log.status
        })
    
    return JsonResponse(logs_data, safe=False)

        
    

def search_records(request):
    form = CompanyModelForm()
    return render(request, 'account/query_builder.html', {'form': form})


@api_view(['GET'])
def count_companies(request):
    industry = request.GET.get('industry')
    size_range = request.GET.get('size_range')
    locality = request.GET.get('locality')
    country = request.GET.get('country')

    count = Company.objects.filter(
        industry=industry,
        size_range=size_range,
        locality=locality,
        country=country
    ).count()
    
    print('count================',count)

    return Response({'count': count})




class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=False, methods=['get'])
    def industry_choices(self, request):
        industries = Company.objects.values_list('industry', flat=True).distinct()
        return Response(industries)

    @action(detail=False, methods=['get'])
    def size_range_choices(self, request):
        size_ranges = Company.objects.values_list('size_range', flat=True).distinct()
        return Response(size_ranges)

    @action(detail=False, methods=['get'])
    def locality_choices(self, request):
        localities = Company.objects.values_list('locality', flat=True).distinct()
        return Response(localities)

    @action(detail=False, methods=['get'])
    def country_choices(self, request):
        countries = Company.objects.values_list('country', flat=True)
        return Response(countries)

class CompanyCountAPIView(APIView):
    serializer_class = CompanyCountSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.GET)
        # pdb.set_trace()
        print('******************************ccccccccc',)
        
        serializer.is_valid(raise_exception=True)
        
        print("Serialized data:", serializer.data)

        filters = serializer.validated_data
        
        print("filters ==",filters)
        
        company_name_filter = filters.pop('name', None)  # Remove this filter from the filters dictionary
        
        
        print('company_name_filter===',company_name_filter)
        
        queryset = Company.objects.filter(**filters)
        
        
        if company_name_filter:
            queryset = queryset.filter(name__contains=company_name_filter)
        
        
        count = queryset.count()
        
        return Response({'count': count})




# class UserListView(APIView):
#     def get(self, request):
#         users = EmailAddress.objects.all()
#         serializer = UserListSerializer(users, many=True)
#         return Response(serializer.data)
    
        
# class UserDetailView(APIView):
#     def get(self, request, user_id):
#         try:
#             user = EmailAddress.objects.get(id=user_id)
#             serializer = UserListSerializer(user)
#             return Response(serializer.data)
#         except EmailAddress.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
            
#     def delete(self, request, user_id):
#         try:
#             user = EmailAddress.objects.get(id=user_id)
#             user.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except EmailAddress.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from allauth.account.models import EmailAddress
# from .serializers import UserProfileSerializer  # Import the serializer



# class UserProfileView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = UserProfileSerializer(user)  # Serialize the user profile data
#         return Response(serializer.data)  # Return a Response instance

#     def put(self, request):
#         user = request.user
#         serializer = UserProfileSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)  # Return a Response instance
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return a Response instance