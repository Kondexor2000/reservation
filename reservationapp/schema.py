import graphene
from .models import Order, NumberPhone
from graphene_django import DjangoObjectType

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "category")

class NumberPhoneType(DjangoObjectType):
    class Meta:
        model = NumberPhone
        fields = ("id", "user", "number_phone")

class Query(graphene.ObjectType):
    my_orders = graphene.List(OrderType)
    my_numbers = graphene.List(NumberPhoneType)

    def resolve_my_orders(self, info):
        user = info.context.user
        return Order.objects.filter(user=user) if user.is_authenticated else Order.objects.none()

    def resolve_my_numbers(self, info):
        user = info.context.user
        return NumberPhone.objects.filter(user=user) if user.is_authenticated else NumberPhone.objects.none()

schema = graphene.Schema(query=Query)
# Mutations tutaj...