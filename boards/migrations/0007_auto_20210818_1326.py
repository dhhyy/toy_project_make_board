# Generated by Django 3.2.6 on 2021-08-18 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_board_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='board',
            name='password',
        ),
        migrations.AddField(
            model_name='board',
            name='depth',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='board',
            name='groupno',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='board',
            name='orderno',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
    ]
