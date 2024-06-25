from django.db import models
from azbankgateways.models import Bank
from azbankgateways.models.enum import PaymentStatus

from accounts.models import User
from subscriptions.models import Package


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
    def __str__(self):
        return f'{self.user} - {self.package} - {self.created_time.strftime("%Y/%m/%d %H-%M")}'