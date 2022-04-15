from django.core import exceptions
from django.db import IntegrityError
from django.http import Http404
from django.urls import reverse_lazy

from proprietor.building.models import Apartment, Building


class ApartmentDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        if not Apartment.objects.filter(pk=self.kwargs['apt_pk']):
            raise Http404
        apartment_owners = Apartment.objects.values_list('owner').get(pk=self.kwargs['apt_pk'])
        if self.request.user.pk not in apartment_owners:
            raise exceptions.PermissionDenied("You don't have permissions to do that")
        return super().dispatch(request, *args, **kwargs)


class UtilityExpenseGetContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class UtilityExpenseFormValidMixin:
    def form_valid(self, form):
        try:
            self.object = form.save()
        except IntegrityError:
            form.add_error(None, 'There is already an Expense with the selected parameters.')
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)


class UtilityExpenseListViewMixin(ApartmentDispatchMixin,
                                  UtilityExpenseGetQuerysetMixin,
                                  UtilityExpenseGetContextMixin):
    """
    A composit class
    """


class UtilityExpenseCreateViewMixin(ApartmentDispatchMixin,
                                    UtilityExpenseGetKwargsFormMixin,
                                    UtilityExpenseGetSuccessUrlMixin,
                                    UtilityExpenseGetContextMixin,
                                    UtilityExpenseFormValidMixin):
    """
    A composit class
    """


class UtilityExpenseEditViewMixin(ApartmentDispatchMixin,
                                  UtilityExpenseGetQuerysetMixin,
                                  UtilityExpenseGetObjectMixin,
                                  UtilityExpenseGetSuccessUrlMixin,
                                  UtilityExpenseGetContextMixin,
                                  UtilityExpenseFormValidMixin):
    """
    A composit class
    """


class UtilityExpenseDeleteViewMixin(ApartmentDispatchMixin,
                                    UtilityExpenseGetQuerysetMixin,
                                    UtilityExpenseGetObjectMixin,
                                    UtilityExpenseGetSuccessUrlMixin):
    """
    A composit class
    """


class ApartmentEditDeleteViewMixin:
    def dispatch(self, request, *args, **kwargs):
        building = Building.objects.get(pk=self.kwargs['pk'])
        if not building.manager == self.request.user:
            raise Http404("You don't have permissions to do that")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        building = Building.objects.get(pk=self.kwargs['pk'])
        queryset = queryset.filter(building=building)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        apt_pk = self.kwargs['apt_pk']
        queryset = queryset.filter(pk=apt_pk)
        apartment_object = queryset.get()
        return apartment_object
