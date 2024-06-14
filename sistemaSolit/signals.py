from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog, Usuario

@receiver(post_save)
def create_or_update_log(sender, instance, created, **kwargs):
    if not isinstance(instance, AuditLog) and sender != Usuario:
        if hasattr(instance, 'modified_by') and instance.modified_by is not None:
            action = 'CREATE' if created else 'UPDATE'
            AuditLog.objects.create(
                user=instance.modified_by,
                action=action,
                model_name=ContentType.objects.get_for_model(sender).model,
                object_id=instance.pk,
                changes=str(instance))
            

@receiver(post_delete)
def delete_log(sender, instance, **kwargs):
    if not isinstance(instance, AuditLog) and sender != Usuario:
        if hasattr(instance, 'modified_by') and instance.modified_by is not None:
            AuditLog.objects.create(
                user=instance.modified_by,
                action='DELETE',
                model_name=ContentType.objects.get_for_model(sender).model,
                object_id=instance.pk,
                changes=str(instance)
            )
