from django.db import models
from django.db.models.fields.related import ForeignKey

class Admin(models.Model):
    admin_title   = models.CharField(max_length=45)
    admin_content = models.CharField(max_length=450)
    hits          = models.SmallIntegerField(default=0)
    create_at     = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    
    class Meta:
        db_table = 'admins'
        
class Board(models.Model):
    title     = models.CharField(max_length=450)
    writer    = ForeignKey('users.User', on_delete=models.CASCADE)
    content   = models.CharField(max_length=500)
    hits      = models.SmallIntegerField(default=0)
    create_at = models.DateField(auto_now_add=True)
    admin     = ForeignKey('boards.Admin', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    
    class Meta:
        db_table = 'boards'