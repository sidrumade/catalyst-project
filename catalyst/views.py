from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Company

from django.core.exceptions import ValidationError


from django.core.files.storage import FileSystemStorage
import pdb
import pandas as pd
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



def clean_data(df):
    df['industry'] = df['industry'].fillna('not available').astype(str)
    df['locality'] = df['locality'].fillna('not available').astype(str)
    df['country'] = df['country'].fillna('not available').astype(str)
    df['linkedin url'] = df['linkedin url'].fillna('not available').astype(str)
    df['domain'] = df['domain'].fillna('not available').astype(str)
    df['name'] = df['name'].fillna('not available').astype(str)
    df['year founded'] = df['year founded'].fillna(0).astype(int)
    if df['domain'].dtype == object :
        df['size range'] = df['size range'].apply(lambda a: a.replace('+',''))
    df['size range'] = df['size range'].fillna('not available').astype(str)
    df['current employee estimate'] = df['current employee estimate'].fillna(0).astype(int)
    df['total employee estimate'] = df['total employee estimate'].fillna(0).astype(int)
    return df


def upload_csv(request):
  """Handles the upload of a CSV file and inserts it into the database."""

  if request.method == 'POST':
    file = request.FILES['datafile']
    
    if not file:
        raise ValidationError("No file selected")

    # Save the file to the filesystem
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    
    
    if not filename.endswith('.csv'):
        raise ValidationError("Invalid file format. Please upload a CSV file.")


    # Read the CSV file and insert the data into the database
    chunk_size = 500000  # Number of rows per chunk
    with open(fs.path(filename), 'r') as csvfile:
        for chunk in pd.read_csv(csvfile, chunksize=chunk_size):
            companies_to_insert = []
            print('processing chunk===================')
            chunk = clean_data(chunk)
            for index, row in chunk.iterrows():
                company = Company(
                    name=row['name'],
                    domain=row['domain'],
                    year_founded=row['year founded'],
                    industry=row['industry'],
                    size_range=row['size range'],
                    locality=row['locality'],
                    country=row['country'],
                    linkedin_url=row['linkedin url'],
                    current_employee_estimate=row['current employee estimate'],
                    total_employee_estimate=row['total employee estimate']
                )
                companies_to_insert.append(company)
            # Insert the companies in bulk
            Company.objects.bulk_create(companies_to_insert)

        
        
        
        


    return redirect('catalyst:home')

  else:
    return render(request, 'account/base.html')