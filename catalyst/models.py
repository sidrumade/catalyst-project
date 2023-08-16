from django.db import models
import datetime

from django.utils import timezone

# Create your models here.

"""
    name , domain , year_founded , industry ,size range(convert into number),
    locality , country , linkedin_url , current_employee_estimate (number) ,
    total_employee_estimate
"""

class Company(models.Model):
    name = models.CharField(null=False,max_length=255)
    domain = models.CharField(null=False,max_length=255)
    year_founded = models.PositiveIntegerField()
    industry = models.CharField(null=False,max_length=255)
    size_range = models.CharField(null=False,max_length=255)
    locality = models.CharField(null=False,max_length=255)
    country = models.CharField(null=False,max_length=255)
    linkedin_url = models.CharField(null=False,max_length=255)
    current_employee_estimate = models.PositiveIntegerField()
    total_employee_estimate = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
    
    
class UploadLog(models.Model):
    user = models.CharField(max_length=250,null=False)
    file_name = models.CharField(max_length=250,null=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    total_rows = models.IntegerField(null=False)
    process_rows = models.IntegerField(null=False)
    status = models.CharField(max_length=50,default='In Progress')
    
    