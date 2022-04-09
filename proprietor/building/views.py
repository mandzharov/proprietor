from django.db.models import Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as gen_views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from proprietor.building.forms import CreateExpenseForm
from proprietor.building.models import Apartment, Building, UtilitiesExpenses


class AllBuildingsView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.ListView):
    permission_required = 'building.view_building'
    model = Building
    template_name = 'building/all_buildings.html'


class MyApartmentsView(LoginRequiredMixin, gen_views.ListView):
    model = Apartment
    template_name = 'building/my_apartments.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class ListUtilityExpensesView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.ListView):
    model = UtilitiesExpenses
    permission_required = 'building.view_utilitiesexpenses'
    template_name = 'building/expenses_list.html'
    paginate_by = 10

    def get_queryset(self):
        apartment = Apartment.objects.get(pk=self.kwargs['apt_pk'])
        queryset = super(ListUtilityExpensesView, self).get_queryset().filter(apartment=apartment).order_by(
            '-bill_year', '-entry_dt')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListUtilityExpensesView, self).get_context_data(object_list=None, **kwargs)
        context['apt_pk'] = self.kwargs['apt_pk']
        context['building_pk'] = self.kwargs['pk']
        return context


class AddUtilityExpenseView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.CreateView):
    model = UtilitiesExpenses
    permission_required = 'building.add_utilitiesexpenses'
    template_name = 'building/add_expense.html'
    form_class = CreateExpenseForm

    def get_form_kwargs(self):
        apt_pk = self.kwargs['apt_pk']
        apt = Apartment.objects.get(pk=apt_pk)
        form_kwargs = super(AddUtilityExpenseView, self).get_form_kwargs()
        form_kwargs['apartment'] = apt
        return form_kwargs

    def get_success_url(self):
        building = self.kwargs['pk']
        apartment = self.kwargs['apt_pk']
        url = reverse_lazy('list expenses', kwargs={'pk': building, 'apt_pk': apartment})
        return url.format(**self.object.__dict__)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['apt_pk'] = self.kwargs['apt_pk']
        context['building_pk'] = self.kwargs['pk']
        return context


class EditUtilityExpenseView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.UpdateView):
    model = UtilitiesExpenses
    permission_required = 'building.change_utilitiesexpenses'
    template_name = 'building/add_expense.html'
    fields = ['utility_type', 'amount', 'bill_year', 'bill_month']

    def get_queryset(self):
        queryset = super(EditUtilityExpenseView, self).get_queryset()
        building = Building.objects.get(pk=self.kwargs['pk'])
        apartment = Apartment.objects.get(pk=self.kwargs['apt_pk'])
        queryset = queryset.filter(apartment__owner=self.request.user).filter(apartment__building=building).filter(
            apartment=apartment)
        return queryset

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs['exp_pk']
        queryset = queryset.filter(pk=pk)
        expense_object = queryset.get()
        return expense_object

    def get_success_url(self):
        building = self.kwargs['pk']
        apartment = self.kwargs['apt_pk']
        url = reverse_lazy('list expenses', kwargs={'pk': building, 'apt_pk': apartment})
        return url.format(**self.object.__dict__)


class DeleteUtilityExpenseView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.DeleteView):
    model = UtilitiesExpenses
    permission_required = 'building.delete_utilitiesexpenses'
    template_name = 'building/delete_expense.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        building = Building.objects.get(pk=self.kwargs['pk'])
        apartment = Apartment.objects.get(pk=self.kwargs['apt_pk'])
        queryset = queryset.filter(apartment__owner=self.request.user).filter(apartment__building=building).filter(
            apartment=apartment)
        return queryset

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs['exp_pk']
        queryset = queryset.filter(pk=pk)
        expense_object = queryset.get()
        return expense_object

    def get_success_url(self):
        building = self.kwargs['pk']
        apartment = self.kwargs['apt_pk']
        url = reverse_lazy('list expenses', kwargs={'pk': building, 'apt_pk': apartment})
        return url.format(**self.object.__dict__)


class ReportView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.View):
    http_method_names = ['get']
    permission_required = 'building.view_utilitiesexpenses'

    def get(self, request, *args, **kwargs):
        queryset = UtilitiesExpenses.objects \
            .filter(apartment__owner=self.request.user) \
            .filter(apartment__building=self.kwargs['pk']) \
            .filter(apartment_id=self.kwargs['apt_pk'])
        year_selected = 'All'
        month_selected = 'All'
        type_selected = 'All'
        if request.GET:
            year_selected = request.GET.get('Year')
            month_selected = request.GET.get('Month').strip()
            type_selected = request.GET.get('Type')
        if not year_selected == 'All':
            queryset = queryset.filter(bill_year=year_selected)
        if not month_selected == 'All':
            queryset = queryset.filter(bill_month=month_selected)
        if not type_selected == 'All':
            queryset = queryset.filter(utility_type__name=type_selected)
        year_choices = queryset.order_by('bill_year').values_list('bill_year').distinct()
        month_choices = queryset.order_by('bill_month').values_list('bill_month').distinct()
        name_choices = queryset.order_by('utility_type__name').values_list('utility_type__name').distinct()
        result = queryset.aggregate(Avg('amount'))
        context = {'year_choices': [str(i[0]) for i in year_choices],
                   'month_choices': [i[0] for i in month_choices],
                   'name_choices': [i[0] for i in name_choices],
                   'year_selected': year_selected,
                   'month_selected': month_selected,
                   'name_selected': type_selected,
                   'result': result['amount__avg']
                   }
        return render(request, template_name='building/report.html', context=context)
