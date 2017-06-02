# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db import transaction
import xlwt, StringIO
from datetime import datetime, tzinfo, timedelta

from models import Employee, Stationery, Order, Items


# Create your views here.


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


class UTC(tzinfo):
    """UTC"""

    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


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
                request.session['len'] = Stationery.objects.all().__len__()
                request.session['itemlist'] = [0] * Stationery.objects.all().__len__()
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
        # self.request.session.itemlist[]
        # page = self.request.GET.get('page')

        # try:
        #     stationerys = self.paginator.page(page)
        #
        # except PageNotAnInteger:  # If page is not an integer, deliver first page.
        #     stationerys = self.paginator.page(1)
        #
        # except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        #     stationerys = self.paginator.page(self.paginator.num_pages)
        stationery = Stationery.objects.all().order_by("id")

        return stationery

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['username'] = self.request.COOKIES.get('username')
        # context['page_num'] = range(1,self.paginator.num_pages+1)
        # context['page_last'] = self.paginator.num_pages
        return context


@transaction.atomic
def order(request):
    # 这里添加验证 不能全是0 网页上也要验证
    orderTemp = Order(employee=Employee.objects.get(name=request.session['username']))
    orderTemp.save()
    for stationery in Stationery.objects.all():
        if request.POST.get(str(stationery.id)) != '0':
            item = Items(stationery=stationery, amount=request.POST[str(stationery.id)], order=orderTemp)
            item.save()

            # print request.POST.get(str(stationery.id))
    ItemList = Items.objects.filter(order=orderTemp)

    return render(request, 'wenjuApp/result.html', {'ItemList': ItemList})


def exportStationeryOrder(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=export_stationerys.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet(u'文具订单')
    # 1st line
    sheet.write(0, 0, 'Stationery')
    sheet.write(0, 1, 'Amount')
    sheet.write(0, 2, 'Employee')
    sheet.write(0, 3, 'Section')
    sheet.write(0, 4, 'Date')

    row = 1
    for item in Items.objects.all():
        sheet.write(row, 0, item.stationery.name)
        sheet.write(row, 1, item.amount)
        sheet.write(row, 2, item.order.employee.name)
        sheet.write(row, 3, item.order.employee.section.name)
        date = item.order.pub_date
        sheet.write(row, 4, date.year.__str__() + "-" + date.month.__str__() + "-" + date.day.__str__())
        row = row + 1

    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response
