# -*- mode: python; coding: utf-8; -*-

from django.conf.urls.defaults import *
from logs import views

info = {}

urlpatterns = patterns(
    '',
    url(r'^$',
        views.index, name="logs"),
    url(r'^top_pages/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.top_pages_day, name="top_pages_day"),
    url(r'^view_depth/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.view_depth_day, name="view_depth_day"),
    url(r'^page_views/(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.page_views_month, name="page_views_month"),
    url(r'^unique_ips/(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.unique_ips_month, name="unique_ips_month"),
    )
