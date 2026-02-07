from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

class NumberPhone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number_phone = models.CharField(max_length=9)