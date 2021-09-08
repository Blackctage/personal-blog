from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True)
    avatar_photo = models.ImageField(upload_to='profile_photo', default='static/main/assets/images/download.jpg')
    website = models.URLField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        ordering = ['user']


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


