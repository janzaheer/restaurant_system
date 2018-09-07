# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from common.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'email',)

    @staticmethod
    def name(obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)

    @staticmethod
    def email(obj):
        return obj.user.email


admin.site.register(UserProfile, UserProfileAdmin)
