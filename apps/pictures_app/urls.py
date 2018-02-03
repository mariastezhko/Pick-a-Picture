from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^upload/?$', views.renderForm),
    url(r'^submitcriteria/?$', views.submitCriteria),
    url(r'^submitsubcategory/?$', views.submitSubcategory),
    url(r'^submitimage/?$', views.submitImage),
    url(r'^login/?$', views.processLogin),
    url(r'^logout/?$', views.logout),
    #url(r'^register/?$', views.processRegistration),
]
