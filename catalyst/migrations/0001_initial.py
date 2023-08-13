# Generated by Django 4.2.4 on 2023-08-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('year_founded', models.PositiveIntegerField()),
                ('industry', models.CharField(max_length=255)),
                ('size_range', models.PositiveIntegerField()),
                ('locality', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('linkedin_url', models.CharField(max_length=255)),
                ('current_employee_estimate', models.PositiveIntegerField()),
                ('total_employee_estimate', models.PositiveIntegerField()),
            ],
        ),
    ]
