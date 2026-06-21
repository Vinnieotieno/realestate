from django.contrib import admin

from realtors.utils import get_realtor_dashboard_context

admin.site.index_template = 'admin/custom_index.html'

_original_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context.update(get_realtor_dashboard_context())
    return _original_index(request, extra_context)


admin.site.index = custom_admin_index
