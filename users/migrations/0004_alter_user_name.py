# Generated by Django 3.2.6 on 2021-08-17 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210817_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
