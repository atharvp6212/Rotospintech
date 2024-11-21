# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, WorkerProfile

@receiver(post_save, sender=User)
def create_worker_profile(sender, instance, created, **kwargs):
    if created and instance.is_worker:
        WorkerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_worker_profile(sender, instance, **kwargs):
    if instance.is_worker:
        instance.workerprofile.save()
