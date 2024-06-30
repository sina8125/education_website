# Django
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# local
from .models import Payment
from subscriptions.models import Package, Subscription

# third party
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException


def go_to_gateway_view(request, package_id):
    package = Package.objects.get(pk=package_id)

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(package.price)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("payments:callback-gateway"))
        bank.set_mobile_number(str(request.user.phone_number).replace(' ', ''))  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()
        Payment.objects.create(user=request.user, package=package, bank=bank_record, amount=package.price)

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        # TODO: redirect to failed page.
        messages.error(request, _('اتصال به درگاه با مشکل مواجه شد'), 'danger')
        return redirect('subscriptions:package_list', )


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        payment = Payment.objects.get(bank=bank_record)
        Subscription.objects.create(package=payment.package, user=payment.user, payment=payment)
    except bank_models.Bank.DoesNotExist:
        raise Http404

    return render(request, 'payments/callback.html',
                  {'package': payment.package, 'bank_record': bank_record})
