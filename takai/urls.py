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

    # session for professors - delete ta
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/prof/(?P<pk>\d+)/delete-ta/$', views.DeleteTa.as_view(), name='ta-delete'),

     # ex: /takai/2018Spring/140/edit/faculty
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/(?P<pk>\d+)/edit/faculty/$', views.UpdateSession.as_view(), name='session-faculty-edit'),

    # ex: /takai/2018Spring/140/edit/mentor
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/(?P<pk>\d+)/edit/mentorsession/$', views.UpdateMentorSession.as_view(), name='session-mentor-edit'),

     # ex: /takai/2018Spring/140/add/mentor
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/(?P<session>[0-9]+)/add/mentorsession/$', views.addMentorSession, name='session-mentor-add'),

    # ex: /takai/2018Spring/140/(ta_id)/edit
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/(?P<cid>[0-9]+)/(?P<pk>\d+)/edit-ta/$', views.UpdateTa.as_view(), name='ta-edit'),

    # ex: /takai/010314573/
    url(r'^(?P<sid>[0-9]{8})/$', views.profile, name='profile'),

    # advanced search
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/search/$', views.adv_search, name='advsearch'),
    url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/searchresults/$', views.adv_search, name='searchresults'),

    # url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/searchresults/$', views.SearchView, name='searchresults'),

    # ex: /takai/apply
     url(r'^(?P<year>[0-9]{4})(?P<semester>[A-Za-z]+)/apply/$', views.TaApplication, name='apply'),

    url(r'^login/$', auth_views.login, name='login'),

    url(r'^admin/', admin.site.urls),

    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),

    url(r'^signup/$', views.signup, name='signup'),
]
