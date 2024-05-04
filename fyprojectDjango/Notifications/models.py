from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField('userapp.AdminUser')
    event = models.ForeignKey ('eventapp.Event', on_delete=models.PROTECT, null=True, blank=True)
    is_read= models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
