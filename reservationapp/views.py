from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import OrderForm, NumberPhoneForm
from .models import NumberPhone


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Już się zalogowałeś/aś :)")
            return redirect('add_order')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Brawo! Masz już swoje konto. Teraz możesz się zalogować :)"
        )
        return response


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('edit_profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profil jest już jak nowy :)")
        return response


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_account.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            "Usunąłeś/aś swoje konto. Mamy nadzieję, że kiedyś do nas wrócisz :)"
        )
        return super().delete(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', False)

        if remember_me:
            self.request.session.set_expiry(1209600)  # 2 tygodnie
        else:
            self.request.session.set_expiry(0)

        messages.success(self.request, "Zalogowałeś/aś się? Świetnie!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_order')


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.info(
            request,
            "Wylogowałeś/aś się! Dobrze, że nie na zawsze :)"
        )
        return super().dispatch(request, *args, **kwargs)


class AssignUserMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddOrderView(LoginRequiredMixin, AssignUserMixin, CreateView):
    form_class = OrderForm
    template_name = 'add_order.html'
    success_url = reverse_lazy('number_phone')


class AddNumberPhoneView(LoginRequiredMixin, AssignUserMixin, CreateView):
    form_class = NumberPhoneForm
    template_name = 'add_number_phone.html'
    success_url = reverse_lazy('number_phone')


class UpdateNumberPhoneView(LoginRequiredMixin, UpdateView):
    model = NumberPhone
    form_class = NumberPhoneForm
    template_name = 'update_number_phone.html'
    success_url = reverse_lazy('number_phone')

    def get_queryset(self):
        return NumberPhone.objects.filter(user=self.request.user)


class DeleteNumberPhoneView(LoginRequiredMixin, DeleteView):
    model = NumberPhone
    template_name = 'delete_number_phone.html'
    success_url = reverse_lazy('number_phone')

    def get_queryset(self):
        return NumberPhone.objects.filter(user=self.request.user)


def number_phone_by_request_user(request):
    template_name = 'read_number_phone.html'

    number_phone = NumberPhone.objects.filter(user=request.user)
    
    return render(
        request,
        template_name,
        {'number_phone': number_phone}
    )