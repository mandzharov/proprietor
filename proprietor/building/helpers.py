from django.http import Http404
from django.urls import reverse_lazy

from proprietor.building.models import Apartment


class UtilityExpenseDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        apartment_owners = Apartment.objects.values_list('owner').get(pk=self.kwargs['apt_pk'])
        if self.request.user.pk not in apartment_owners:
            raise Http404("You don't have permissions to do that")
        return super().dispatch(request, *args, **kwargs)


class UtilityExpenseGetContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['apt_pk'] = self.kwargs['apt_pk']
        context['building_pk'] = self.kwargs['pk']
        return context


class UtilityExpenseGetQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        apartment = Apartment.objects.get(pk=self.kwargs['apt_pk'])
        queryset = queryset.filter(apartment=apartment).order_by('-bill_year', '-entry_dt')
        return queryset


class UtilityExpenseGetKwargsFormMixin:
    def get_form_kwargs(self):
        apt_pk = self.kwargs['apt_pk']
        apt = Apartment.objects.get(pk=apt_pk)
        form_kwargs = super().get_form_kwargs()
        form_kwargs['apartment'] = apt
        return form_kwargs


class UtilityExpenseGetSuccessUrlMixin:
    def get_success_url(self):
        building = self.kwargs['pk']
        apartment = self.kwargs['apt_pk']
        url = reverse_lazy('list expenses', kwargs={'pk': building, 'apt_pk': apartment})
        return url.format(**self.object.__dict__)


class UtilityExpenseGetObjectMixin:
    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs['exp_pk']
        queryset = queryset.filter(pk=pk)
        expense_object = queryset.get()
        return expense_object


class UtilityExpenseListViewMixin(UtilityExpenseDispatchMixin,
                                  UtilityExpenseGetQuerysetMixin,
                                  UtilityExpenseGetContextMixin):
    """
    A combination class
    """


class UtilityExpenseCreateViewMixin(UtilityExpenseDispatchMixin,
                                    UtilityExpenseGetKwargsFormMixin,
                                    UtilityExpenseGetSuccessUrlMixin,
                                    UtilityExpenseGetContextMixin):
    """
    A combination class
    """


class UtilityExpenseEditViewMixin(UtilityExpenseDispatchMixin,
                                  UtilityExpenseGetQuerysetMixin,
                                  UtilityExpenseGetObjectMixin,
                                  UtilityExpenseGetSuccessUrlMixin,
                                  UtilityExpenseGetContextMixin):
    """
    A combination class
    """


class UtilityExpenseDeleteViewMixin(UtilityExpenseDispatchMixin,
                                    UtilityExpenseGetQuerysetMixin,
                                    UtilityExpenseGetObjectMixin,
                                    UtilityExpenseGetSuccessUrlMixin):
    """
    A combination class
    """
