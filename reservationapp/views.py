from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages
import graphene
from graphene_django.types import DjangoObjectType

from .forms import OrderForm, NumberPhoneForm 
from .models import NumberPhone, Order, Category
import logging

logger = logging.getLogger(__name__)

def check_template(template_name, request):
    try:
        get_template(template_name)
        logger.info(f"Template '{template_name}' found.")
        return True
    except TemplateDoesNotExist:
        logger.error(f"Template '{template_name}' does not exist.")
        return False

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not check_template(self.template_name, request):
            return HttpResponse("Template not found.")
        if request.user.is_authenticated:
            messages.info(request, "You are already registered and logged in.")
            return redirect('add-post')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful. Please log in.")
        return response

class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('add-post')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully.")
        return response

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_account.html'
    success_url = reverse_lazy('login_existing')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user
        raise Http404("You are not logged in.")

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Account deleted successfully.")
            return response
        except Exception as e:
            logger.error(f"An error occurred during account deletion: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('delete_account')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not check_template(self.template_name, self.request):
            return HttpResponse("Template not found.")
        
        remember_me = form.cleaned_data.get('remember_me', False)
        if remember_me:
            self.request.session.set_expiry(1209600)  
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_post')

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

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
        logger.warning(f"Template '{template_name}' not found for user {request.user}.")
        return HttpResponseNotFound("Template not found.")
    
    number_phone = NumberPhone.objects.filter(user=request.user)

    try:
        number_phone = NumberPhone.objects.filter(user=request.user)
        logger.info(f"Number Phone retrieved successfully for user {request.user}.")
    except Exception as e:
        logger.error(f"Error retrieving categories for user {request.user}: {e}")
    
    return render(request, template_name, {'number_phone': number_phone})

def orders_by_request_user(request):
    template_name = 'read_orders.html'
    if not check_template(template_name, request):
        logger.warning(f"Template '{template_name}' not found for user {request.user}.")
        return HttpResponseNotFound("Template not found.")

    try:
        order = Order.objects.filter(user=request.user)
        logger.info(f"Order retrieved successfully for user {request.user}.")
    except Exception as e:
        logger.error(f"Error retrieving categories for user {request.user}: {e}")

    return render(request, template_name, {'order': order})

# --- Typy oparte o modele ---
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "category")  # tylko istniejące pola

class NumberPhoneType(DjangoObjectType):
    class Meta:
        model = NumberPhone
        fields = ("id", "user", "number_phone")  # poprawna nazwa

# --- Query (odpowiedniki widoków read) ---
class Query(graphene.ObjectType):
    my_orders = graphene.List(OrderType)
    my_numbers = graphene.List(NumberPhoneType)

    def resolve_my_orders(self, info):
        user = info.context.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def resolve_my_numbers(self, info):
        user = info.context.user
        if user.is_authenticated:
            return NumberPhone.objects.filter(user=user)
        return NumberPhone.objects.none()
    
# --- Mutacje dla Order ---
class CreateOrder(graphene.Mutation):
    class Arguments:
        category_id = graphene.ID(required=True)  # zamiast product/quantity

    order = graphene.Field(OrderType)

    def mutate(self, info, category_id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Musisz być zalogowany")
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Exception("Kategoria nie istnieje")

        order = Order(user=user, category=category)
        order.save()
        return CreateOrder(order=order)

class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        user = info.context.user
        try:
            order = Order.objects.get(id=id, user=user)
            order.delete()
            return DeleteOrder(ok=True)
        except Order.DoesNotExist:
            return DeleteOrder(ok=False)

# --- Mutacje dla NumberPhone ---
class CreateNumberPhone(graphene.Mutation):
    class Arguments:
        number_phone = graphene.String(required=True)  # poprawiona nazwa

    number = graphene.Field(NumberPhoneType)

    def mutate(self, info, number_phone):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Musisz być zalogowany")
        number = NumberPhone(user=user, number_phone=number_phone)
        number.save()
        return CreateNumberPhone(number=number)

class UpdateNumberPhone(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        number_phone = graphene.String(required=True)

    number = graphene.Field(NumberPhoneType)

    def mutate(self, info, id, number_phone):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Musisz być zalogowany")

        try:
            number = NumberPhone.objects.get(id=id, user=user)
        except NumberPhone.DoesNotExist:
            raise Exception("Numer nie istnieje")

        number.number_phone = number_phone
        number.save()
        return UpdateNumberPhone(number=number)

# --- Root Mutations ---
class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    delete_order = DeleteOrder.Field()
    create_number_phone = CreateNumberPhone.Field()
    update_number_phone = UpdateNumberPhone.Field()