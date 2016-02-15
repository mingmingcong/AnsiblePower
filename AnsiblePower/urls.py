"""AnsiblePower URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from base.views import Index
from adhoc.views import AdHocList, AdHocDetail, AdHocExecute, AdhocLog, AdhocDelete
from job.views import AnsibleJobList,AnsibleJobDetail,AnsibleJobExecuete,AnsibleJobLog

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', Index.as_view()),

    url(r'^adhoc/$', AdHocList.as_view(), name='adhoc_list'),
    url(r'^adhoc/(?P<adhoc_id>[0-9]+)/$', AdHocDetail.as_view()),
    url(r'^adhoc/add/$', AdHocExecute.as_view(), name='adhoc_add'),
    url(r'^adhoc/delete/$', AdhocDelete.as_view(), name='adhoc_delete'),
    url(r'^adhoc/log/$', AdhocLog.as_view(), name='adhoc_log'),

    url(r'^job/$',AnsibleJobList.as_view(),name='job_list'),
    url(r'^job/(?P<job_id>[0-9]+)/$',AnsibleJobDetail.as_view()),
    url(r'^job/add/$',AnsibleJobExecuete.as_view(),name='job_add'),
    # url(r'job/delete/$',An)
    url(r'^job/log/$',AnsibleJobLog.as_view(),name='job_log')
]
