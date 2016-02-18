from django.shortcuts import render
# Create your views here.
import simplejson
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, HttpResponse


class Login(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.POST.get('next','')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = next_url
        else:
            redirect_url = '/'
        return HttpResponseRedirect(redirect_url)


class Logout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        next_url = request.GET.get('next','')
        return HttpResponseRedirect(next_url)
