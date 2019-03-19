# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone


class DatedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(
        default=timezone.now, blank=True, null=True
    )


class UserProfile(models.Model):
    USER_TYPE_OWNER = 'owner'
    USER_TYPE_CASHIER = 'cashier'
    USER_TYPE_STOCK = 'stock'

    USER_TYPES = (
        (USER_TYPE_OWNER, 'Owner'),
        (USER_TYPE_CASHIER, 'Cashier'),
        (USER_TYPE_STOCK, 'Stock Manager'),
    )

    user = models.OneToOneField(User, related_name='user_profile')
    user_type = models.CharField(
        max_length=100, choices=USER_TYPES, default=USER_TYPE_OWNER
    )
    address = models.TextField(max_length=512, blank=True, null=True)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    mobile_no = models.CharField(max_length=13, blank=True, null=True)
    picture = models.ImageField(
        upload_to='images/profile/picture/', max_length=1024, blank=True
    )
    date_of_birth = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username


# Signal Functions
def create_profile(sender, instance, created, **kwargs):
    """
    The functions used to check if user profile is not created
    and created the user profile without saving role and hospital
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not UserProfile.objects.filter(user=instance):
        return UserProfile.objects.create(
            user=instance,
            user_type=UserProfile.USER_TYPE_OWNER
        )


# Signals
post_save.connect(create_profile, sender=User)

