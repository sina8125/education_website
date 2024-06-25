from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import User


class Package(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    duration = models.DurationField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'package'
        verbose_name_plural = 'packages'

    def get_absolute_url(self):
        return reverse('subscriptions:package_detail', args=[self.pk,])


class Subscription(models.Model):
    from payments.models import Payment

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='subscriptions', null=False,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', null=False, blank=False)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, related_name='subscriptions', null=True)
    start_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'

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
        return f'Subscription of {self.user} to {self.package}'
