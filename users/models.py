from django.db import models

class User(models.Model):
    user_email    = models.CharField(max_length=45)
    user_password = models.CharField(max_length=45)
    user_name     = models.CharField(max_length=45)
    create_at     = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'