from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages

from .forms import OrderForm, NumberPhoneForm 
from .models import NumberPhone
import logging

logger = logging.getLogger(__name__)

def check_template(template_name, request):
    try:
        get_template(template_name)
        logger.info(f"Plik .html znaleziony")
        return True
    except TemplateDoesNotExist:
        logger.error(f"Gdzie jest plik .html?")
        return False

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Gdzie jest plik .html?")
        if request.user.is_authenticated:
            messages.info(request, "Już się zalogowałeś/aś :)")
            return redirect('add_order')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Brawo! Masz już swoje konto. Teraz możesz się zalogować :)")
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
        if self.request.user.is_authenticated:
            return self.request.user
        raise Http404("Zapomniałeś się zalogować?")

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Usunąłeś/aś swoje konto. Mamy nadzieję, że kiedyś do nas wrócisz :)")
            return response
        except Exception as e:
            logger.error(f"Wyskoczył taki błąd: {str(e)}")
            messages.error(request, f"Wyskoczył taki błąd: {str(e)}")
            return redirect('delete_account')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not check_template(self.template_name, self.request):
            return HttpResponse("Gdzie jest plik .html?")
        
        remember_me = form.cleaned_data.get('remember_me', False)
        if remember_me:
            self.request.session.set_expiry(1209600)  
        messages.success(self.request, "Zalogowałeś/aś się? Świetnie!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_order')

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Wylogowałeś/aś się! Dobrze, że nie na zawsze :)")
        return super().dispatch(request, *args, **kwargs)

class AddOrderView(LoginRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = 'add_order.html'
    success_url = reverse_lazy('number_phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Gdzie jest plik .html?")
        return super().dispatch(request, *args, **kwargs)

class AddNumberPhoneView(LoginRequiredMixin, CreateView):
    form_class = NumberPhoneForm
    template_name = 'add_number_phone.html'
    success_url = reverse_lazy('number_phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Gdzie jest plik .html?")
        return super().dispatch(request, *args, **kwargs)

class UpdateNumberPhoneView(LoginRequiredMixin, UpdateView):
    model = NumberPhone
    form_class = NumberPhoneForm
    template_name = 'update_number_phone.html'
    success_url = reverse_lazy('number_phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Gdzie jest plik .html?")
        return super().dispatch(request, *args, **kwargs)
    
class DeleteNumberPhoneView(LoginRequiredMixin, DeleteView):
    model = NumberPhone
    template_name = 'delete_number_phone.html'
    success_url = reverse_lazy('number_phone')

    def get_object(self, queryset=None):
        pk_id = self.kwargs.get('pk')
        return get_object_or_404(NumberPhone, id=pk_id, user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Gdzie jest plik .html?")
        return super().dispatch(request, *args, **kwargs)

def number_phone_by_request_user(request):
    template_name = 'read_number_phone.html'
    if not check_template(template_name, request):
        logger.warning(f"Gdzie jest plik .html?")
        return HttpResponseNotFound("Gdzie jest plik .html?")
    
    number_phone = NumberPhone.objects.filter(user=request.user)

    try:
        number_phone = NumberPhone.objects.filter(user=request.user)
        logger.info(f"Numer telefonu wdrożony")
    except Exception as e:
        logger.error(f"Wyskoczył jakiś błąd: {str(e)}")
    
    return render(request, template_name, {'number_phone': number_phone})