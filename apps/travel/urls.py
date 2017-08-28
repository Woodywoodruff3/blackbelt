from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^destination/(?P<id>\d+)', views.show),
    url(r'^join/(?P<id>\d+)', views.join),
    url(r'^add$', views.add),
    url(r'^addplan$', views.addplan)
]