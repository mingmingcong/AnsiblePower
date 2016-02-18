# coding=utf-8
import simplejson
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic import View
from django.template.loader import render_to_string
from django.template import RequestContext
from django.db.models import Q
from adhoc.models import AnsibleAdhoc, AnsibleModule, AnsibleAdhocTask
from adhoc.tasks import run_adhoc
from host.models import AnsibleGroup, AnsibleHost
from common.utils import playbook_list_hosts, model_to_inventory


# Create your views here.


class AdHocList(LoginRequiredMixin, TemplateView):
    page_size = 10

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        query = request.GET.get('query', '')

        if query:
            adhocs = AnsibleAdhoc.objects.filter(Q(adhoc_args__contains=query) | Q(adhoc_pattern__contains=query) |
                                                 Q(adhoc_name__contains=query) | Q(id=query))
        else:
            adhocs = AnsibleAdhoc.objects.all()
        paginator = Paginator(adhocs, self.page_size)

        # paginate
        try:
            adhocs = paginator.page(page)
        except PageNotAnInteger:
            adhocs = paginator.page(1)
        except InvalidPage:
            adhocs = paginator.page(paginator.num_pages)

        res_ctx = {}
        res_ctx.update(adhocs=adhocs)
        res_ctx.update(modules=AnsibleModule.objects.filter(module_name='shell'))

        patterns = []
        patterns.extend([{'name': '[GROUP] %s' % group.group_name, 'value': group.group_name} for group in
                         AnsibleGroup.objects.all()])
        patterns.extend(
            [{'name': '[HOST][%s] %s %s' % (host.ansible_group.group_name, host.hostname, host.ip), 'value': host.ip}
             for host in AnsibleHost.objects.all()])
        patterns.insert(0, {'name': '[ALL]', 'value': 'all'})
        res_ctx.update(patterns=patterns)

        if query:
            res_ctx.update(query=query)
        return render(request, 'adhoc.html', res_ctx)


class AdHocDetail(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        adhoc_id = kwargs.get('adhoc_id', 1)
        adhoc = AnsibleAdhoc.objects.select_related().get(id=adhoc_id)
        res_ctx = {}
        try:
            res_ctx.update(adhoc=adhoc)
        except AnsibleAdhoc.DoesNotExist:
            pass
            # 404
        if request.is_ajax():
            if adhoc.finish:
                adhoc_finish = True
            else:
                adhoc_finish = False
            res = render_to_string('adhoc_detail_part.html', res_ctx, context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'result': res, 'status': 0, 'finish': adhoc_finish}),
                                content_type='application/json')

        else:

            return render(request, 'adhoc_detail.html', res_ctx)


class AdhocDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        adhoc_id = request.POST.get('adhoc_id', '')
        if request.is_ajax():
            AnsibleAdhoc.objects.filter(id=adhoc_id).delete()
            return HttpResponse(simplejson({'result': '', 'status': 0}))


class AdhocLog(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        adhoc_task_id = request.GET.get('adhoc_task_id', '')
        print adhoc_task_id
        if request.is_ajax():
            try:
                adhoc_task = AnsibleAdhocTask.objects.get(id=adhoc_task_id)
            except:
                pass
                # 404
            res_ctx = {}
            res_ctx.update(log=adhoc_task.stderr if adhoc_task.stderr else adhoc_task.stdout,
                           task_host=adhoc_task.task_host)

            return HttpResponse(simplejson.dumps({'result': res_ctx, 'status': 0}), content_type='application/json')


class AdHocExecute(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        adhoc_name = request.POST.get('adhoc_name', '')
        adhoc_pattern = request.POST.get('adhoc_pattern', '')
        adhoc_args = request.POST.get('adhoc_args', '')
        module_id = request.POST.get('module_id', '')
        adhoc_id = request.POST.get('adhoc_id', '')
        start_time = timezone.now()

        if request.is_ajax():
            adhoc_old = AnsibleAdhoc.objects.get(id=adhoc_id)
            adhoc = AnsibleAdhoc.objects.create(adhoc_name=adhoc_old.adhoc_name, adhoc_pattern=adhoc_old.adhoc_pattern,
                                                adhoc_args=adhoc_old.adhoc_args,
                                                ansible_module=adhoc_old.ansible_module, start_time=start_time,
                                                auth_user_id=request.user.id)

        else:
            adhoc = AnsibleAdhoc.objects.create(adhoc_name=adhoc_name, adhoc_pattern=adhoc_pattern,
                                                adhoc_args=adhoc_args,
                                                ansible_module_id=module_id, start_time=start_time,
                                                auth_user_id=request.user.id)


        inventory_path = model_to_inventory(AnsibleGroup.objects.all())
        # insert adhoc task
        for host in playbook_list_hosts(adhoc.adhoc_pattern, inventory_path):
            AnsibleAdhocTask.objects.create(task_host=host, ansible_adhoc_id=adhoc.id, start_time=timezone.now())

        # use celery to execute an adhoc async
        kwargs = dict(
            instance_type=AnsibleAdhoc.__name__,
            task_id=adhoc.id,
            hosts=adhoc.adhoc_pattern,
            module_args=adhoc.adhoc_args,
            module_name=str(adhoc.ansible_module.module_name),
            inventory_path=inventory_path
        )

        run_adhoc.delay(**kwargs)

        if request.is_ajax():
            res_ctx = {}
            res_ctx.update(adhoc_id=adhoc.id)
            return HttpResponse(simplejson.dumps({'result': res_ctx, 'status': 0, 'finish': adhoc.finish}),
                                content_type='application/json')
        else:
            return HttpResponseRedirect('/adhoc/%d' % adhoc.id)
