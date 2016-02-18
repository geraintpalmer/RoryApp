from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'reinforcementlearning.views.index', name='home'),
    url(r'^about/$',
    	TemplateView.as_view(template_name='about.html'),
    	name='about'),
    url(r'^contact/$',
    	TemplateView.as_view(template_name='contact.html'),
    	name='contact'),
    url(r'^RL/$',
        TemplateView.as_view(template_name='RL.html'),
        name='RL'),
    url(r'^links/$',
        TemplateView.as_view(template_name='links.html'),
        name='links'),
    url(r'^explanation/$',
        TemplateView.as_view(template_name='explanation.html'),
        name='explanation'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^createboard/', 'reinforcementlearning.views.createboard', name='createboard'),
    url(r'^boardlist$', 'reinforcementlearning.views.boardlist', name='boardlist'),
    url(r'^(?P<slug>[-\w\d]+)/$', 'reinforcementlearning.views.theboard', name='theboard'),
    url(r'^(?P<slug>[-\w\d]+)/results', 'reinforcementlearning.views.results', name='results'),
    url(r'^(?P<slug>[-\w\d]+)/(?P<col>[0-9]+)/(?P<row>[0-9]+)', 'reinforcementlearning.views.learninggraphs', name='learninggraphs'),
)
