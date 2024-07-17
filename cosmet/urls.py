"""
URL configuration for cosmet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cosmetapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('', views.AddOrderView.as_view(), name='add_order'),
    path('add-number-phone/', views.AddNumberPhoneView.as_view(), name='add_number_phone'),
    path('update-number-phone/<int:pk>/', views.UpdateNumberPhoneView.as_view(), name='update_number_phone'),
    path('number-phone/', views.number_phone_by_request_user, name='number_phone'),
    path('orders/', views.orders_by_request_user, name='orders'),
]