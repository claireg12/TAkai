from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /takai/
    url(r'^$', views.index, name='index'),
               
    # this doesn't work
    # ex: /takai/5/
    url(r'^(?P<cid>[0-9]+)/$', views.detail, name='detail'),
    # ex: /takai/5/results/
    url(r'^(?P<cid>[0-9]+)/results/$', views.results, name='results'),
    # ex: /takai/5/vote/
    url(r'^(?P<cid>[0-9]+)/vote/$', views.vote, name='vote'),
]
