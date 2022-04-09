from django import forms

from proprietor.building.models import UtilitiesExpenses


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

