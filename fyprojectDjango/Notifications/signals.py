from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from basedataapp.utils import get_parent_structures
from eventapp.models import Event
from Notifications.models import Notification
from Notifications.serializers import NotificationSerializer
from userapp.models import AdminUser


@receiver(post_save, sender=Event)
def create_notification(sender, instance, created, **kwargs):
    if created:
        struct=instance.work.installation.structure.id
        users_list = []
        current_structure = get_parent_structures(struct)
        id_struct=[struct.id for struct in current_structure]
        users_list= AdminUser.objects.filter(structure__in=id_struct)
        users_id=[user.id for user in users_list]
        notification={
            "title": f'New Event is created by {instance.created_by} ',
            "description": f'this is from event {instance.label} created by {instance.created_by}',
            "event": instance.id,
            "users": users_id,
        }
        notify, createed= Notification.objects.get_or_create(title=notification['title'], description=notification['description'], event=instance)
        notify.users.set(users_id)
