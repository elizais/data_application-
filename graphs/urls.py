from django.urls import include, path
from . import views
from graphs.dash_apps.finished_apps import ValueTemp

urlpatterns = [
    path('', views.plot, name='plot'),
]