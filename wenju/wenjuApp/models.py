# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=200)


class Employee(models.Model):
    name = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    password = models.CharField(max_length=20)
    month_flag = models.BooleanField(default=True)


class Stationery(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=10)
    photo = models.CharField(max_length=200)  # path


class Order(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Items(models.Model):
    stationery = models.ForeignKey(Stationery)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
