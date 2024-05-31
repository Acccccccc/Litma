from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Literature, Attachment

@receiver(pre_delete, sender=Literature)
def delete_attachments_with_literature(sender, instance, **kwargs):
    attachments = Attachment.objects.filter(literature=instance)
    for attachment in attachments:
        attachment.delete()
