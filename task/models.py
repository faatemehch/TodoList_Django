from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task( models.Model ):
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    title_task = models.CharField( max_length=250 )
    date_added = models.DateTimeField( auto_now_add=True )
    complete = models.BooleanField( default=False )

    def __str__(self):
        return self.title_task

    class Meta:
        ordering = ['date_added']
