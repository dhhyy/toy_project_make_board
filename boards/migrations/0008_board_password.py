# Generated by Django 3.2.6 on 2021-08-18 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_auto_20210818_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='password',
            field=models.CharField(default=None, max_length=5000),
        ),
    ]
