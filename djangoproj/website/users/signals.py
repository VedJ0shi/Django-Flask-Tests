#implements automatic Profile instance creation for every new User created
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

'''User model is the 'sender' of signal to the 'receiver' '''

@receiver(post_save, sender=User) #when new User created, post_save signal is sent to receiver
def create_profile(sender, instance, created, **kwargs): #instance refers to instance of User
    if created:
        Profile.objects.create(user=instance)
'''create_profile function is the receiver'''

@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    instance.profile.save()