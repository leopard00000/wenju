from django.conf.urls import url

from . import views

app_name = 'wenjuApp'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^order/$', views.order, name='order'),
]
