from __future__ import absolute_import , unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

import gc

import pandas as pd

from .models import Company , UploadLog

from django.core.files.storage import FileSystemStorage
from django.db.models import F
from django.utils import timezone



logger = get_task_logger(__name__)


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


@shared_task
def process_file_upload(temp_folder,filename, username):
    fs = FileSystemStorage(location=temp_folder)

    row_count=0
    with open(fs.path(filename), 'r') as csvfile:
        row_count = sum(1 for row in csvfile)
    log_entry = UploadLog(user = username , file_name = filename , total_rows = row_count - 1 , process_rows = 0 ) 
    log_entry.save()

    logger.info('Task Started For uploading data ============================')
    # Read the CSV file and insert the data into the database
    chunk_size = 100000  # Number of rows per chunk
    with open(fs.path(filename), 'r') as csvfile:
        for chunk in pd.read_csv(csvfile, chunksize=chunk_size):
            companies_to_insert = []
            logger.info('processing chunk===================')
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
            
            UploadLog.objects.filter(id=log_entry.id).update(process_rows=F('process_rows') + chunk.shape[0]  )
            gc.collect()

        UploadLog.objects.filter(id=log_entry.id).update(end_time = timezone.now()  , status = 'Complete')

