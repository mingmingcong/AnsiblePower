from __future__ import division
import simplejson
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.generic import TemplateView, View
from job.models import AnsibleJob, AnsibleJobTask
from playbook.models import AnsiblePlaybook
from host.models import AnsibleGroup,AnsibleHost
from common.utils import playbook_list_hosts, playbook_generate_yaml,model_to_inventory
from tasks import run_job


# Create your views here.


class AnsibleJobList(TemplateView):
    page_size = 10

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        query = request.GET.get('query', '')

        if query:
            jobs = AnsibleJob.objects.filter(Q(job_name__contains=query) | Q(job_pattern__contains=query))
        else:
            jobs = AnsibleJob.objects.all()
        paginator = Paginator(jobs, self.page_size)

        # paginate
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except InvalidPage:
            jobs = paginator.page(paginator.num_pages)

        res_ctx = {}
        res_ctx.update(jobs=jobs)
        res_ctx.update(templates=AnsiblePlaybook.objects.all())

        patterns = []
        patterns.extend([{'name':'[GROUP] %s'%group.group_name,'value':group.group_name} for group in AnsibleGroup.objects.all()])
        patterns.extend([{'name':'[HOST][%s] %s<%s>'%(host.ansible_group.group_name,host.hostname,host.ip),'value':host.ip} for host in AnsibleHost.objects.all()])
        patterns.insert(0,{'name':'[ALL]','value':'all'})
        res_ctx.update(patterns=patterns)

        if query:
            res_ctx.update(query=query)

        return render(request, 'job.html', res_ctx)


class AnsibleJobDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id', 1)
        res_ctx = {}
        try:

            job = AnsibleJob.objects.select_related().get(id=job_id)
        except AnsibleJob.DoesNotExist:
            pass
            # 404

        res_ctx.update(job=job)

        host_status = []
        hosts = set([task.task_host for task in AnsibleJobTask.objects.filter(ansible_job_id=job.id)])
        for host in hosts:
            # compute progress bar
            all_tasks = AnsibleJobTask.objects.filter(ansible_job_id=job_id, task_host=host)
            finished_tasks = set([task for task in all_tasks if task.finish == True])
            progress_percent = int(len(finished_tasks) / all_tasks.count() * 100)

            # get running task
            if all_tasks.count() != len(finished_tasks):
                processing_task = all_tasks.filter(finish=False).first()
                processing_index = len(finished_tasks) + 1
            else:
                processing_index = None
                processing_task = None

            # get start_time and end_time
            if all_tasks.count() > 0:
                start_time = all_tasks.first().start_time
                if job.finish:
                    end_time = all_tasks.last().end_time
                else:
                    end_time = None

            host_status.append(
                dict(
                    ip=host,
                    progress_percent=progress_percent,
                    start_time=start_time,
                    end_time=end_time,
                    processing_index=processing_index,
                    processing_task=processing_task,
                    all=all_tasks.count(),
                    success=all_tasks.filter(failure=False, finish=True).count()
                )
            )

        res_ctx.update(hosts=host_status)

        if request.is_ajax():
            if job.finish:
                job_finish = True
            else:
                job_finish = False
            res = render_to_string('job_detail_part.html', res_ctx, context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'result': res, 'status': 0, 'finish': job_finish}),
                                content_type='application/json')

        else:

            return render(request, 'job_detail.html', res_ctx)


class AnsibleJobLog(TemplateView):
    def get(self, request, *args, **kwargs):
        job_id = request.GET.get('job_id', '')
        host = request.GET.get('host', '')
        job_tasks = AnsibleJobTask.objects.filter(ansible_job_id=job_id, task_host=host)
        res_ctx = {}
        res_ctx.update(job_tasks=job_tasks)
        res = render_to_string('job_detail_log.html', res_ctx, context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'result': res, 'status': 0, 'host': host}),
                            content_type='application/json')


class AnsibleJobExecuete(View):
    def post(self, request, *args, **kwargs):
        job_name = request.POST.get('job_name', '')
        job_pattern = request.POST.get('job_pattern', '')
        template_id = request.POST.get('template_id', '')
        start_time = timezone.now()

        if request.is_ajax():
            pass
        else:
            job = AnsibleJob.objects.create(job_name=job_name, job_pattern=job_pattern, start_time=start_time,
                                            ansible_playbook_id=template_id)
            for host in playbook_list_hosts(job.job_pattern):
                AnsibleJobTask.objects.bulk_create([
                                                       AnsibleJobTask(task_name=task.task_name,
                                                                      task_host=host,
                                                                      ansible_job_id=job.id,
                                                                      start_time=start_time)
                                                       for task in
                                                       job.ansible_playbook.ansibleplaybooktask_set.all()
                                                       ]
                                                   )

        inventory_path = model_to_inventory(AnsibleGroup.objects.all())
        playbook_template = AnsiblePlaybook.objects.get(id=template_id)
        kwargs = dict(
            instance_type=AnsibleJob.__name__,
            task_id=job.id,
            hosts=job.job_pattern,
            inventory_path=inventory_path
        )

        run_job.delay(playbook_generate_yaml(playbook_template), **kwargs)
        return HttpResponseRedirect('/job/%d' % job.id)
