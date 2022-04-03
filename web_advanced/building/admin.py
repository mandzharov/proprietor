from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from web_advanced.building.models import Apartment, Building, UtilitiesExpenses, BuildingExpenses, BuildingIncome, \
    UtilityType


class ApartmentInline(admin.StackedInline):
    model = Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    inlines = [
        ApartmentInline,
    ]


@admin.register(UtilitiesExpenses)
class UtilitiesExpensesAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingExpenses)
class BuildingExpensesAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingIncome)
class BuildingIncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(UtilityType)
class UtilityTypeAdmin(admin.ModelAdmin):
    pass
