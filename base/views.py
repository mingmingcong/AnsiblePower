from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView


class Index(TemplateView):


    def get(self, request, *args, **kwargs):
        return render(request,'index.html')