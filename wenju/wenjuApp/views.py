# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from models import Employee, Stationery


# Create your views here.


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = Employee.objects.filter(name__exact=username, password__exact=password)
            if user:
                response = HttpResponseRedirect(reverse('wenjuApp:index'))
                request.session['username'] = username
                request.session['itemlist'] = [0]*Stationery.objects.all().__len__()
                return response
            else:
                return HttpResponseRedirect(reverse('wenjuApp:login'))
    else:
        uf = UserForm()
    return render(request, 'wenjuApp/login.html', {'uf': uf})


class IndexView(generic.ListView):

    template_name = 'wenjuApp/index.html'
    context_object_name = 'stationerys'
    # paginator = Paginator(Stationery.objects.all(), 6)

    def get_queryset(self):
        #self.request.session.itemlist[]
        # page = self.request.GET.get('page')

        # try:
        #     stationerys = self.paginator.page(page)
        #
        # except PageNotAnInteger:  # If page is not an integer, deliver first page.
        #     stationerys = self.paginator.page(1)
        #
        # except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        #     stationerys = self.paginator.page(self.paginator.num_pages)
        stationery = Stationery.objects.all()

        return stationery


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['username'] = self.request.COOKIES.get('username')
        # context['page_num'] = range(1,self.paginator.num_pages+1)
        # context['page_last'] = self.paginator.num_pages
        return context


def order(request):
    return HttpResponse("OK")
