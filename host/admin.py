from django.contrib import admin
# Register your models here.
from django.contrib import admin
from host.models import AnsibleGroup, AnsibleHost, AnsibleVariable


class HostInline(admin.TabularInline):
    model = AnsibleHost
    fields = ('hostname', 'ip',)
    extra = 1


class VariableInline(admin.TabularInline):
    model = AnsibleVariable
    fields = ('variable_key', 'variable_value')
    extra = 1


class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ip', 'ansible_group')
    fields = ('hostname', 'ip', 'ansible_group', 'username')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name',)
    inlines = [
        HostInline,
        VariableInline
    ]


admin.site.register(AnsibleGroup, GroupAdmin)
admin.site.register(AnsibleHost, HostAdmin)
