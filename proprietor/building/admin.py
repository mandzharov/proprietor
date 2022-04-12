from django.contrib import admin

from proprietor.building.models import Apartment, Building, UtilitiesExpenses, BuildingExpenses, BuildingIncome, \
    UtilityType


class ApartmentInline(admin.StackedInline):
    model = Apartment
    max_num = 2


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('building', 'floor', 'number')


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    inlines = [
        ApartmentInline,
    ]


@admin.register(UtilitiesExpenses)
class UtilitiesExpensesAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'utility_type', 'bill_year', 'bill_month')


@admin.register(BuildingExpenses)
class BuildingExpensesAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingIncome)
class BuildingIncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(UtilityType)
class UtilityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
