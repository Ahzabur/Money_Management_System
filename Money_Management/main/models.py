from django.db import models
from django.contrib.auth.models import User


class Cash(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    source = models.CharField(max_length=100)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Expense(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.CharField(max_length=200)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
