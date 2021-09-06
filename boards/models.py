from django.db import models
from django.db.models.fields.related import ForeignKey
        
class Board(models.Model):
    title     = models.CharField(max_length=100)
    content   = models.CharField(max_length=500)
    password  = models.CharField(max_length=5000, default=None)
    hits      = models.PositiveIntegerField(default=0)
    groupno   = models.IntegerField(default=0)
    orderno   = models.IntegerField(default=0)
    depth     = models.IntegerField(default=0)
    writer    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    tag       = models.ForeignKey('Tag', on_delete=models.CASCADE)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    
    class Meta:
        db_table = 'boards'
        
class Tag(models.Model):
    name = models.CharField(max_length=50, default=None)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.name)
    
    class Meta:
        db_table = 'tags'