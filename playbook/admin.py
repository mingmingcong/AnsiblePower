from django.contrib import admin
# Register your models here.
from django.contrib import admin
from playbook.models import AnsibleModule, AnsiblePlaybook, AnsiblePlaybookHandler, AnsiblePlaybookTask


class PlaybookHandlerInline(admin.TabularInline):
    model = AnsiblePlaybookHandler
    fields = ('handler_name', 'ansible_module', 'module_args')
    extra = 1


class PlaybookTaskInline(admin.TabularInline):
    model = AnsiblePlaybookTask
    fields = ('task_name', 'ansible_module', 'module_args','ignore_errors','task_notify')
    extra = 1


class PlaybookAdmin(admin.ModelAdmin):
    list_display = ('playbook_name',)
    fieldsets = (
        ('Basic', {
            'fields': ('playbook_name',)
        }),
    )
    inlines = [
        PlaybookTaskInline,
        PlaybookHandlerInline
    ]


admin.site.register(AnsiblePlaybook, PlaybookAdmin)
