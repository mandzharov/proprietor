from django.contrib.auth import get_user_model, authenticate, login
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as gen_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from web_advanced.registration.forms import RegistrationForm, CreateProfileForm, LoginForm
from web_advanced.registration.models import Profile

AppUserModel = get_user_model()


class AppLoginView(auth_views.LoginView):
    next_page = reverse_lazy('login success')
    authentication_form = LoginForm


def login_success(request):
    if Profile.objects.filter(pk=request.user.pk):
        return redirect("home page")
    else:
        return redirect("create profile")


class AppLogoutView(auth_views.LogoutView):
    template_name = 'registration/logout.html'


class AppRegisterView(gen_views.CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login success')

    def form_valid(self, form):
        form.save()
        email = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return redirect(self.success_url)


class AddProfileView(auth_mixins.LoginRequiredMixin, gen_views.CreateView):
    form_class = CreateProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('home page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditProfileView(auth_mixins.LoginRequiredMixin, gen_views.UpdateView):
    template_name = 'registration/edit_profile.html'
    model = Profile
    fields = [
        'first_name',
        'middle_name',
        'last_name',
        'birth_date',
        'gender',
        'phone',
        'picture',
        'phone_code',
    ]
    success_url = reverse_lazy('home page')


class DeleteProfileView(auth_mixins.LoginRequiredMixin, gen_views.DeleteView):
    model = AppUserModel
    success_url = reverse_lazy('home page')
    template_name = 'registration/delete_profile.html'


@receiver(pre_delete, sender=AppUserModel)
def delete_profile_on_user_delete(sender, instance, *args, **kwargs):
    if instance.profile:
        print(f'The profile will be deleted')
        print(f'{instance.profile.first_name} {instance.profile.last_name}')
