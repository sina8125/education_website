from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from subscriptions.models import Package


class PackageView(View):
    def get(self, request):
        packages = Package.objects.all()
        return render(request, 'subscriptions/package.html', {'packages': packages})


class PackageDetailView(View):
    @method_decorator(login_required)
    def get(self, request, package_id):
        package = get_object_or_404(Package, pk=package_id, is_active=True)
        return render(request, 'subscriptions/package_detail.html', context={'package': package})