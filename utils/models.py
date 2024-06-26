from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractCreatedUpdatedTime(models.Model):
    created_time = models.DateTimeField(
        verbose_name=_('زمان ایجاد'),
        auto_now_add=True
    )
    updated_time = models.DateTimeField(
        verbose_name=_('آخرین تغییر'),
        auto_now=True
    )

    class Meta:
        abstract = True
