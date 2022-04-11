from django import forms

from proprietor.building.models import UtilitiesExpenses, UtilityType, Apartment


class CreateExpenseForm(forms.ModelForm):

    def __init__(self, apartment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apartment = apartment

    def save(self, commit=True):
        expense = super().save(commit=False)
        expense.apartment = self.apartment
        if commit:
            expense.save()
        return expense

    class Meta:
        model = UtilitiesExpenses
        fields = ['utility_type', 'bill_year', 'bill_month', 'amount']


class CreateUtilityForm(forms.ModelForm):
    class Meta:
        model = UtilityType
        fields = '__all__'


class CreateApartmentForm(forms.ModelForm):

    def __init__(self, building, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = building

    def save(self, commit=True):
        apartment = super().save(commit=False)
        apartment.building = self.building
        if commit:
            apartment.save()
        return apartment

    class Meta:
        model = Apartment
        exclude = ('building',)
