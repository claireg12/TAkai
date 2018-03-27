from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /takai/
    url(r'^$', views.index, name='index'),
               
    # this doesn't work
    # ex: /takai/5/
    url('<int:cid_id>/', views.detail, name='detail'),
    # ex: /takai/5/results/
    url('<int:cid_id>/results/', views.results, name='results'),
    # ex: /takai/5/vote/
    url('<int:cid_id>/vote/', views.vote, name='vote'),
]
