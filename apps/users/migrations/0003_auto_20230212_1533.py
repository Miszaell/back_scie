# Generated by Django 3.2 on 2023-02-12 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230130_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='create_uid',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='update_uid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='create_uid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='update_uid',
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='date_of_birth',
            field=models.DateField(blank=True, default='2000-01-01', max_length=255, null=True, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, default='2000-01-01', max_length=255, null=True, verbose_name='Fecha de nacimiento'),
        ),
    ]
