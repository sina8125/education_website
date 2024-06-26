# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from accounts.models import User
from subscriptions.models import Package
from utils.models import AbstractCreatedUpdatedTime

# third party
from azbankgateways.models import Bank


class Payment(AbstractCreatedUpdatedTime):
    user = models.ForeignKey(
        User,
        verbose_name=_('کاربر'),
        on_delete=models.CASCADE
    )
    package = models.ForeignKey(
        Package,
        verbose_name=_('بسته'),
        on_delete=models.CASCADE
    )
    bank = models.ForeignKey(
        Bank,
        verbose_name=_('بانک'),
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name=_('مبلغ')
    )

    class Meta:
        verbose_name = _('پرداخت')
        verbose_name_plural = _('پرداخت ها')

    def __str__(self):
        return f'{self.user} - {self.package} - {self.created_time.strftime("%Y/%m/%d %H-%M")}'
