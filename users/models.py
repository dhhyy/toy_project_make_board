from django.db import models

class User(models.Model):
    email     = models.CharField(max_length=45)
    password  = models.TextField()
    name      = models.CharField(max_length=10, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'