from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic as gen_views

from proprietor.building.models import Building, Apartment
from proprietor.register.models import Profile

AppUser = get_user_model()


class HomePageView(gen_views.ListView):
    queryset = Building.objects.all()
    template_name = 'home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        manager_ids = Building.objects.filter(manager__isnull=False).values_list('manager_id').distinct()
        managers = Profile.objects.filter(user__in=manager_ids)
        context.update({'managers_list': managers})
        return context


class ManagerAdminView(LoginRequiredMixin, gen_views.TemplateView):
    template_name = 'manager_admin.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home page')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        my_buildings = Building.objects.filter(manager=self.request.user).prefetch_related('apartment_set')
        assigned_users = Apartment.objects.filter(owner__isnull=False).values_list('owner').distinct()
        pending_users = AppUser.object.exclude(pk__in=assigned_users)
        context.update({'buildings_list': my_buildings, 'pending_users': pending_users})
        return context
