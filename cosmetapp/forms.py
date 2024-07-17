from django import forms
from .models import NumberPhone, Order, Category

class NumberPhoneForm(forms.ModelForm):
    class Meta:
        model = NumberPhone
        fields = ['number_phone']

class OrderForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple # lub inny widget, np. forms.SelectMultiple
    )

    class Meta:
        model = Order
        fields = ['category']