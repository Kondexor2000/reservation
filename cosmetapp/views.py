from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages

from .forms import OrderForm, NumberPhoneForm  # Zakładając, że masz te formularze zdefiniowane w forms.py
from .models import NumberPhone, Order  # Zakładając, że masz te modele zdefiniowane w models.py

# Funkcja pomocnicza do sprawdzania, czy szablon istnieje
def check_template(template_name, request):
    try:
        get_template(template_name)
        return True
    except TemplateDoesNotExist:
        return False

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Brak pliku .html")

        if request.user.is_authenticated:
            return redirect('logout')

        return super().dispatch(request, *args, **kwargs)

class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('add-order')

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Brak pliku .html")

        if not request.user.is_authenticated:
            messages.error(request, 'Nie jesteś zalogowany.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_account.html'
    success_url = reverse_lazy('login_existing')

    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Brak pliku .html")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_authenticated:
            return user
        else:
            raise Http404("Nie jesteś zalogowany.")

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f"Wystąpił błąd: {str(e)}")
            return redirect('delete_account')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not check_template(self.template_name, self.request):
            return HttpResponse("Brak pliku .html")
        
        remember_me = form.cleaned_data.get('remember_me', False)
        if remember_me:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_order')

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'

class AddOrderView(LoginRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = 'add_order.html'
    success_url = reverse_lazy('store-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Brak pliku .html")
        return super().dispatch(request, *args, **kwargs)

class AddNumberPhoneView(LoginRequiredMixin, CreateView):
    form_class = NumberPhoneForm
    template_name = 'add_number_phone.html'
    success_url = reverse_lazy('number-phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Brak pliku .html")
        return super().dispatch(request, *args, **kwargs)

class UpdateNumberPhoneView(LoginRequiredMixin, UpdateView):
    model = NumberPhone
    form_class = NumberPhoneForm
    template_name = 'update_number_phone.html'
    success_url = reverse_lazy('number-phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Brak pliku .html")
        return super().dispatch(request, *args, **kwargs)

def number_phone_by_request_user(request):
    template_name = 'read_number_phone.html'
    if not check_template(template_name, request):
        return HttpResponse("Brak pliku .html")
    
    number_phone = NumberPhone.objects.filter(user=request.user)
    return render(request, template_name, {'number_phone': number_phone})

def orders_by_request_user(request):
    template_name = 'read_orders.html'
    if not check_template(template_name, request):
        return HttpResponse("Brak pliku .html")

    order = Order.objects.filter(user=request.user)
    return render(request, template_name, {'order': order})