from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField('userapp.AdminUser', through='Notification_User')
    event = models.ForeignKey ('eventapp.Event', on_delete=models.PROTECT, null=True, blank=True)
    is_read= models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notification_schema"."notification'

class Notification_User(models.Model):
    user = models.ForeignKey('userapp.AdminUser', on_delete=models.PROTECT)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user_name

    class Meta:
        db_table = 'notification_schema"."notification_user'
    
