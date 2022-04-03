from django.contrib import admin
from django.contrib.auth import get_user_model

from web_advanced.registration.models import Profile

AppUserModel = get_user_model()


@admin.register(AppUserModel)
class AppUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
