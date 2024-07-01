import jdatetime
from django.utils import timezone
from django.utils.translation import get_language
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf.locale.es import formats as es_formats
from django.utils import formats


class CreatedUpdatedTimeAdminMixin:
    list_display = ['created_time', 'updated_time']
    readonly_fields = ['created_time', 'updated_time']

    @admin.display(description=_('زمان ایجاد'))
    def jcreated_time(self, obj):
        return jdatetime.datetime.fromgregorian(
            datetime=obj.created_time.astimezone(tz=timezone.get_current_timezone()), tzinfo=timezone.tzinfo,
            locale=jdatetime.FA_LOCALE).strftime('%-d %B %Y، ساعت %H:%M')

    @admin.display(description=_('آخرین تغییر'))
    def jupdated_time(self, obj):
        return jdatetime.datetime.fromgregorian(
            datetime=obj.updated_time.astimezone(tz=timezone.get_current_timezone()), tzinfo=timezone.tzinfo,
            locale=jdatetime.FA_LOCALE).strftime('%-d %B %Y، ساعت %H:%M')

    def get_list_display(self, request):
        list_display = super().get_list_display(request) if hasattr(super(), 'get_list_display') else []
        list_display = list(list_display)
        if get_language().lower() == 'fa-ir':
            if 'created_time' in list_display:
                list_display.remove('created_time')
                list_display.append('jcreated_time')
            if 'updated_time' in list_display:
                list_display.remove('updated_time')
                list_display.append('jupdated_time')

        return list_display

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request) if hasattr(super(), 'get_readonly_fields') else []
        readonly_fields = list(readonly_fields)
        if get_language().lower() == 'fa-ir':
            if 'created_time' in readonly_fields:
                readonly_fields.remove('created_time')
                readonly_fields.append('jcreated_time')
            if 'updated_time' in readonly_fields:
                readonly_fields.remove('updated_time')
                readonly_fields.append('jupdated_time')
        return readonly_fields
