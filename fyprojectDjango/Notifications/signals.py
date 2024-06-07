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
        struct = instance.created_by.structure.id
        users_list = []
        current_structure = get_parent_structures(struct)
        id_struct = [s.id for s in current_structure]

        # Get all admin users in the current structures
        users_list = AdminUser.objects.filter(structure__in=id_struct)

        # Initialize users_id list with the instance creator's ID
        users_id = [instance.created_by.id]

        # Append all admin user IDs to the users_id list
        for user in users_list:
            users_id.append(user.id)

        notification = {
            "title": "An Event has occured at Structure: "
            + instance.work.installation.structure.label
            + "\n"
            + "Company: "
            + instance.work.installation.structure.company.label
            + "\n"
            + "created by "
            + instance.created_by.user_name,
            "description": f"An Event has occured at \nStructure: {instance.work.installation.structure} \nCompany: {instance.work.installation.structure.company}\n By: {instance.created_by}\n at: {instance.start_date}\n this event to sent to all the users on the onward Hierarchy of the structure.",
            "event": instance.id,
            "users": users_id,
        }

        # Create or get the Notification instance
        notify, created = Notification.objects.get_or_create(
            title=notification["title"],
            description=notification["description"],
            event=instance,
        )

        # Set the users for the Notification
        notify.users.set(users_id)
        notify.save()
