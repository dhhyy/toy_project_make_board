# Generated by Django 3.2.6 on 2021-08-17 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_rename_admin_id_board_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
