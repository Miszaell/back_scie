# Generated by Django 3.2 on 2023-02-12 21:59

import apps.base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230212_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='r_object',
            field=models.JSONField(default=apps.base.models.get_r_object, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='r_object',
            field=models.JSONField(default=apps.base.models.get_r_object, null=True),
        ),
    ]
