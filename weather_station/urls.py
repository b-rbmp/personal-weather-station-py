from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:station_id>/', views.station, name="station"),
    path('<int:station_id>/history/<int:day_from>-<int:month_from>-<int:year_from>/<int:day_to>-<int:month_to>-<int:year_to>', views.history, name="history"),
    path('sobre/', views.sobre, name="sobre"),
]
