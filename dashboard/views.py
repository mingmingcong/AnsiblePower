from django.shortcuts import render, HttpResponse
from django.utils import timezone
from datetime import timedelta, datetime
# Create your views here.
from django.views.generic import TemplateView
from host.models import AnsibleHost, AnsibleGroup
from adhoc.models import AnsibleAdhoc
from job.models import AnsibleJob
from playbook.models import AnsiblePlaybook
from collections import OrderedDict
import simplejson


class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):


        res_ctx = {}

        res_ctx.update(groups=AnsibleGroup.objects.all().count())
        res_ctx.update(hosts=AnsibleHost.objects.all().count())
        res_ctx.update(commands=AnsibleAdhoc.objects.all().count())
        res_ctx.update(jobs=AnsibleJob.objects.all().count())
        res_ctx.update(playbooks=AnsiblePlaybook.objects.all().count())

        start_time = timezone.now() + timedelta(days=-30)

        # recent commands
        recent_commands = AnsibleAdhoc.objects.filter(start_time__gt=start_time).order_by('start_time')
        recent_commands_dict = OrderedDict()
        for command in recent_commands:
            command_starttime = datetime.strftime(command.start_time, '%Y-%m-%d')
            try:
                recent_commands_dict[command_starttime] += 1
            except KeyError:
                recent_commands_dict[command_starttime] = 0
                recent_commands_dict[command_starttime] += 1
        recent_commands = dict(
            count=[recent_commands_dict[key] for key in recent_commands_dict],
            date=[key for key in recent_commands_dict]
        )
        res_ctx.update(recent_commands=recent_commands)

        # recnet jobs
        recent_jobs_dict = OrderedDict()
        recent_jobs = AnsibleJob.objects.filter(start_time__gt=start_time).order_by('start_time')
        for job in recent_jobs:
            job_starttime = datetime.strftime(job.start_time, '%Y-%m-%d')
            try:
                recent_jobs_dict[job_starttime] += 1
            except KeyError:
                recent_jobs_dict[job_starttime] = 0
                recent_jobs_dict[job_starttime] += 1

        recent_jobs = dict(
            count=[recent_jobs_dict[key] for key in recent_jobs_dict],
            date=[key for key in recent_jobs_dict]
        )
        res_ctx.update(recent_jobs=recent_jobs)
        return HttpResponse(simplejson.dumps(res_ctx), content_type='application/json')
