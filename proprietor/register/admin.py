from django.contrib import admin
from django.contrib.auth import get_user_model

from proprietor.register.models import CountryCodes, Profile

AppUserModel = get_user_model()


@admin.register(AppUserModel)
class AppUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user')


@admin.register(CountryCodes)
class CountryCodesAdmin(admin.ModelAdmin):
    pass
