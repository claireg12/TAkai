from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # ex: /takai/ --> /takai/2018Spring/
    url(r'^$', RedirectView.as_view(url='/takai/2018Spring/')),
        
    # ex: /takai/2018Spring/
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/$', views.semester, name='semester'),
               
    # ex: /takai/2018Spring/140/
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/$', views.session, name='session'),
           
#    # ex: /takai/5/
#    url(r'^(?P<cid>[0-9]+)/$', views.detail, name='detail'),

    
    
               
    #url(r'^(?P<year>[0-9]{4})/(?P<semester>[a-z]{4,6})/(?P<cid>[0-9]+)/$', views.session, name='session'),

]
