from django.conf.urls import url
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # ex: /takai/ --> /takai/2018Spring/
    url(r'^$', RedirectView.as_view(url='/takai/2018Spring/')),

    # ex: /takai/2018Spring/
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/$', views.semester, name='semester'),

    # ex: /takai/2018Spring/140/
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/$', views.session, name='session'),


    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/enroll/$', views.enroll, name='session-enroll'),
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/teach/$', views.teach, name='session-teach'),

    # session for professors (can add TAs)
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/prof/$', views.prof, name='session-prof'),

    # ex: /takai/010314573/
    url(r'^(?P<sid>[0-9]{8})/$', views.profile, name='profile'),

    # ex: /takai/search/
    url(r'^search/$', views.search, name='search'),


    url(r'^login/$', auth_views.login, name='login'),

    url(r'^admin/', admin.site.urls),

    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
]
