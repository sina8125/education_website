# Django
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# local
from accounts.models import User
from utils.models import AbstractCreatedUpdatedTime
from utils.utils import translate_field


class Package(AbstractCreatedUpdatedTime):
    title = models.CharField(
        verbose_name=_('عنوان فارسی'),
        max_length=200,
        null=False
    )
    title_en = models.CharField(
        verbose_name=_('عنوان انگلیسی'),
        max_length=200,
        null=False
    )
    description = models.TextField(
        verbose_name=_('توضیحات فارسی'),
        blank=True,
        null=True
    )
    description_en = models.TextField(
        verbose_name=_('توضیحات انگلیسی'),
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name=_('وضعیت بسته'),
        default=True
    )
    price = models.PositiveIntegerField(
        verbose_name=_('قیمت')
    )
    duration = models.DurationField(
        verbose_name=_('مدت زمان'),
        blank=True,
        null=True
    )

    def __str__(self):
        return translate_field(self, 'title')

    class Meta:
        verbose_name = _('بسته')
        verbose_name_plural = _('بسته ها')

    def get_absolute_url(self):
        return reverse('subscriptions:package_detail', args=[self.pk, ])


class Subscription(AbstractCreatedUpdatedTime):
    from payments.models import Payment

    package = models.ForeignKey(
        Package,
        verbose_name=_('بسته'),
        on_delete=models.CASCADE,
        related_name='subscriptions',
        null=False,
        blank=False
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('کاربر'),
        on_delete=models.CASCADE,
        related_name='subscriptions',
        null=False,
        blank=False
    )
    payment = models.ForeignKey(
        Payment,
        verbose_name=_('پرداخت'),
        on_delete=models.SET_NULL,
        related_name='subscriptions',
        null=True
    )
    start_time = models.DateTimeField(
        verbose_name=_('زمان شروع'),
        default=timezone.now
    )
    expire_time = models.DateTimeField(
        verbose_name=_('زمان پایان'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('اشتراک')
        verbose_name_plural = _('اشتراک ها')

    @property
    def is_expired(self):
        if self.expire_time:
            return timezone.now() > self.expire_time
        return False

    @property
    def remaining_time(self):
        if self.expire_time:
            return self.expire_time - timezone.now()

    def save(self, *args, **kwargs):
        if self.package and self.package.duration:
            if not self.expire_time:
                if self.start_time:

                    self.expire_time = self.package.duration + self.start_time
                else:
                    self.expire_time = self.package.duration + timezone.now()
        # else:
        #     self.expire_time = None
        super().save(*args, **kwargs)

    def __str__(self):
        return _('اشتراک {} برای کاربر {}').format(self.package, self.user)
