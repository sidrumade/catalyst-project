# Generated by Django 4.2.4 on 2023-08-15 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst', '0004_alter_uploadlog_end_time_alter_uploadlog_start_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadlog',
            old_name='fila_name',
            new_name='file_name',
        ),
        migrations.AlterField(
            model_name='uploadlog',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='uploadlog',
            name='status',
            field=models.CharField(default='In Progress', max_length=50),
        ),
    ]
