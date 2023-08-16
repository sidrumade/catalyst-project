from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.exceptions import ValidationError


from django.core.files.storage import FileSystemStorage

import pdb

from .tasks import process_file_upload

from .models import UploadLog , Company

from django.http import JsonResponse

from .forms import CompanyModelForm



# Create your views here.



class UserProfileView(LoginRequiredMixin, TemplateView):
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
    if request.method == 'POST':
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            selected_data = form.cleaned_data
            counts = Company.objects.filter(
                industry=selected_data['industry'],
                size_range=selected_data['size_range'],
                locality=selected_data['locality'],
                country=selected_data['country']
            ).count()
            return render(request, 'account/query_builder.html', {'counts': counts , 'form':form})
    else:
        form = CompanyModelForm()
        
    return render(request, 'account/query_builder.html', {'form': form})








