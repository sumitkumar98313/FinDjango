from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# this signal runs every time a User object is saved
# if it's a brand new user, we create a Profile for them automatically
# this is better than creating the profile manually in every view
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # only create profile for new users not on every save
        Profile.objects.create(user=instance)


# this makes sure profile is saved whenever user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
