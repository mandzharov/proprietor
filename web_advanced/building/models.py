from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.deconstruct import deconstructible


UserModel = get_user_model()


@deconstructible
class EmptyApartmentValidator:
    def __init__(self, entry_type):
        self.entry_type = entry_type

    def __call__(self, value):
        if not value and self.entry_type == 'Subscription':
            raise ValidationError('When the type is "Subscription", the "Apartment" cannot be empty!')


class Building(models.Model):
    city = models.CharField(max_length=30)
    street_address = models.CharField(max_length=60)
    block_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    floors_count = models.IntegerField()
    alias = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.street_address} {self.block_number}'


class Apartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor = models.IntegerField(validators=[MinValueValidator(0)])
    area = models.FloatField(validators=[MinValueValidator(0)])
    rooms_count = models.IntegerField(validators=[MinValueValidator(0)])
    share = models.FloatField()
    description = models.TextField(null=True, blank=True)
    owner = models.ManyToManyField(UserModel)


class UtilityType(models.Model):
    # UTILITIES = (
    #     'Electricity',
    #     'Water',
    #     'Gas',
    #     'Heating',
    #     'Internet',
    #     'TV',
    #     'Phone',
    #     'Communal',
    #     'Taxes',
    #     'Other',
    # )
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)


class UtilitiesExpenses(models.Model):
    MONTH_CHOICES = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'Jun'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    ]

    name = models.ForeignKey(UtilityType, on_delete=models.PROTECT)
    bill_year = models.IntegerField(validators=[MinValueValidator(1981), MaxValueValidator(2099)])
    bill_month = models.CharField(max_length=3, choices=MONTH_CHOICES, null=True, blank=True)
    entry_dt = models.DateTimeField(auto_now=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)


class BuildingExpenses(models.Model):
    TYPES = (
        'Housekeeping',
        'Planned',
        'Emergency',
        'Salary',
        'Other',
    )
    TYPE_CHOICES = [(i, i) for i in TYPES]

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=max(len(i) for i in TYPES), choices=TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    payment_date = models.DateField()
    entry_dr = models.DateTimeField(auto_now_add=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)


class BuildingIncome(models.Model):
    TYPES = (
        'Subscription',
        'Rent',
        'Other',
    )
    TYPE_CHOICES = [(i, i) for i in TYPES]

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=max(len(i) for i in TYPES), choices=TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    deposit_date = models.DateField()
    entry_dr = models.DateTimeField(auto_now_add=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
