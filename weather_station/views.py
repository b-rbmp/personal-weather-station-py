from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

import plotly.graph_objects as go
import datetime
import pandas as pd

from .models import WeatherStation
from .forms import DateHistoryForm


def index(request):
    station_list = get_list_or_404(WeatherStation)
    context = {
        'station_list': station_list,
    }
    return render(request, 'weather_station/index.html', context)


def station(request, station_id):
    context = {
        'station': '',
        'graph_temperature': '',
        'graph_luminosity': '',
        'graph_humidity': '',
        'graph_pressure': '',
    }
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DateHistoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            # redirect to a new URL:
            return HttpResponseRedirect(
                reverse('history', args=(
                    station_id,
                    date_from.day, date_from.month, date_from.year,
                    date_to.day, date_to.month, date_to.year,
                )))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DateHistoryForm()
        try:
            station = WeatherStation.objects.get(pk=station_id)
            date_from = datetime.datetime.now() - datetime.timedelta(days=1)
            records_last_day = pd.DataFrame(
                list(
                    station.weatherrecord_set.filter(
                        record_date__gte=date_from).values()))

            config = dict({
                'scrollZoom': False,
                'displayModeBar': False,
                'responsive': True
            })

            fig_temperature = go.Figure([
                go.Scatter(x=records_last_day['record_date'],
                           y=records_last_day['temperature'])
            ])
            fig_temperature.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="#fff",
                plot_bgcolor="#fff",
                xaxis_tickformat='%H:%M',
                hovermode="x unified",
                dragmode=False,
            )
            fig_temperature.update_traces(mode="markers+lines",
                                          hovertemplate=None)
            fig_temperature.update_xaxes(showgrid=True,
                                         gridwidth=1,
                                         gridcolor='rgba(0, 0, 0, 0.15)')
            fig_temperature.update_yaxes(showgrid=True,
                                         gridwidth=1,
                                         gridcolor='rgba(0, 0, 0, 0.15)',
                                         ticksuffix=' °C')
            graph_temperature = fig_temperature.to_html(full_html=False,
                                                        config=config)

            fig_luminosity = go.Figure([
                go.Scatter(x=records_last_day['record_date'],
                           y=records_last_day['light'])
            ])
            fig_luminosity.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="#fff",
                plot_bgcolor="#fff",
                xaxis_tickformat='%H:%M',
                hovermode="x unified",
                dragmode=False,
            )
            fig_luminosity.update_traces(mode="markers+lines",
                                         hovertemplate=None)
            fig_luminosity.update_xaxes(showgrid=True,
                                        gridwidth=1,
                                        gridcolor='rgba(0, 0, 0, 0.15)')
            fig_luminosity.update_yaxes(showgrid=True,
                                        gridwidth=1,
                                        gridcolor='rgba(0, 0, 0, 0.15)',
                                        ticksuffix=' lux')
            graph_luminosity = fig_luminosity.to_html(full_html=False,
                                                      config=config)

            fig_humidity = go.Figure([
                go.Scatter(x=records_last_day['record_date'],
                           y=records_last_day['humidity'])
            ])
            fig_humidity.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="#fff",
                plot_bgcolor="#fff",
                xaxis_tickformat='%H:%M',
                hovermode="x unified",
                dragmode=False,
            )
            fig_humidity.update_traces(mode="markers+lines",
                                       hovertemplate=None)
            fig_humidity.update_xaxes(showgrid=True,
                                      gridwidth=1,
                                      gridcolor='rgba(0, 0, 0, 0.15)')
            fig_humidity.update_yaxes(showgrid=True,
                                      gridwidth=1,
                                      gridcolor='rgba(0, 0, 0, 0.15)',
                                      ticksuffix=' %')
            graph_humidity = fig_humidity.to_html(full_html=False,
                                                  config=config)

            fig_pressure = go.Figure([
                go.Scatter(x=records_last_day['record_date'],
                           y=records_last_day['pressure'])
            ])
            fig_pressure.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="#fff",
                plot_bgcolor="#fff",
                xaxis_tickformat='%H:%M',
                hovermode="x unified",
                dragmode=False,
            )
            fig_pressure.update_traces(mode="markers+lines",
                                       hovertemplate=None)
            fig_pressure.update_xaxes(showgrid=True,
                                      gridwidth=1,
                                      gridcolor='rgba(0, 0, 0, 0.15)')
            fig_pressure.update_yaxes(showgrid=True,
                                      gridwidth=1,
                                      gridcolor='rgba(0, 0, 0, 0.15)',
                                      ticksuffix=' hPa')
            graph_pressure = fig_pressure.to_html(full_html=False,
                                                  config=config)
        except (KeyError, WeatherStation.DoesNotExist):
            context = {
                'station': '',
                'graph_temperature': '',
                'graph_luminosity': '',
                'graph_humidity': '',
                'graph_pressure': '',
            }
        else:
            context = {
                'station': station,
                'graph_temperature': graph_temperature,
                'graph_luminosity': graph_luminosity,
                'graph_humidity': graph_humidity,
                'graph_pressure': graph_pressure,
            }

    context['form'] = form
    return render(request, 'weather_station/station_detail.html', context)


# def update_sensor(request):


def history(request, station_id, day_from, month_from, year_from, day_to,
            month_to, year_to):
    try:
        station = WeatherStation.objects.get(pk=station_id)
        records_last_day = pd.DataFrame(
            list(
                station.weatherrecord_set.filter(
                    record_date__gte=datetime.datetime(day=day_from,
                                                       month=month_from,
                                                       year=year_from,
                                                       hour=0,
                                                       minute=0,
                                                       second=0)).
                filter(record_date__lte=datetime.datetime(day=day_to,
                                                          month=month_to,
                                                          year=year_to,
                                                          hour=23,
                                                          minute=59,
                                                          second=59)).values()))

        config = dict({
            'scrollZoom': False,
            'displayModeBar': False,
            'responsive': True
        })

        fig_temperature = go.Figure([
            go.Scatter(x=records_last_day['record_date'],
                       y=records_last_day['temperature'])
        ])
        fig_temperature.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#fff",
            plot_bgcolor="#fff",
            xaxis_tickformat='%d-%m-%Y<br>%H:%M',
            hovermode="x unified",
            dragmode=False,
        )
        fig_temperature.update_traces(mode="markers+lines", hovertemplate=None)
        fig_temperature.update_xaxes(showgrid=True,
                                     gridwidth=1,
                                     gridcolor='rgba(0, 0, 0, 0.15)')
        fig_temperature.update_yaxes(showgrid=True,
                                     gridwidth=1,
                                     gridcolor='rgba(0, 0, 0, 0.15)',
                                     ticksuffix=' °C')
        graph_temperature = fig_temperature.to_html(full_html=False,
                                                    config=config)

        fig_luminosity = go.Figure([
            go.Scatter(x=records_last_day['record_date'],
                       y=records_last_day['light'])
        ])
        fig_luminosity.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#fff",
            plot_bgcolor="#fff",
            xaxis_tickformat='%d-%m-%Y<br>%H:%M',
            hovermode="x unified",
            dragmode=False,
        )
        fig_luminosity.update_traces(mode="markers+lines", hovertemplate=None)
        fig_luminosity.update_xaxes(showgrid=True,
                                    gridwidth=1,
                                    gridcolor='rgba(0, 0, 0, 0.15)')
        fig_luminosity.update_yaxes(showgrid=True,
                                    gridwidth=1,
                                    gridcolor='rgba(0, 0, 0, 0.15)',
                                    ticksuffix=' lux')
        graph_luminosity = fig_luminosity.to_html(full_html=False,
                                                  config=config)

        fig_humidity = go.Figure([
            go.Scatter(x=records_last_day['record_date'],
                       y=records_last_day['humidity'])
        ])
        fig_humidity.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#fff",
            plot_bgcolor="#fff",
            xaxis_tickformat='%d-%m-%Y<br>%H:%M',
            hovermode="x unified",
            dragmode=False,
        )
        fig_humidity.update_traces(mode="markers+lines", hovertemplate=None)
        fig_humidity.update_xaxes(showgrid=True,
                                  gridwidth=1,
                                  gridcolor='rgba(0, 0, 0, 0.15)')
        fig_humidity.update_yaxes(showgrid=True,
                                  gridwidth=1,
                                  gridcolor='rgba(0, 0, 0, 0.15)',
                                  ticksuffix=' %')
        graph_humidity = fig_humidity.to_html(full_html=False, config=config)

        fig_pressure = go.Figure([
            go.Scatter(x=records_last_day['record_date'],
                       y=records_last_day['pressure'])
        ])
        fig_pressure.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#fff",
            plot_bgcolor="#fff",
            xaxis_tickformat='%d-%m-%Y<br>%H:%M',
            hovermode="x unified",
            dragmode=False,
        )
        fig_pressure.update_traces(mode="markers+lines", hovertemplate=None)
        fig_pressure.update_xaxes(showgrid=True,
                                  gridwidth=1,
                                  gridcolor='rgba(0, 0, 0, 0.15)')
        fig_pressure.update_yaxes(showgrid=True,
                                  gridwidth=1,
                                  gridcolor='rgba(0, 0, 0, 0.15)',
                                  ticksuffix=' hPa')
        graph_pressure = fig_pressure.to_html(full_html=False, config=config)
    except (WeatherStation.DoesNotExist):
        context = {
            'station': '',
            'graph_temperature': '',
            'graph_luminosity': '',
            'graph_humidity': '',
            'graph_pressure': '',
            'day_from': day_from,
            'month_from': month_from,
            'year_from': year_from,
            'day_to': day_to,
            'month_to': month_to,
            'year_to': year_to,
        }
    except (KeyError):
        context = {
            'station': station,
            'graph_temperature': '',
            'graph_luminosity': '',
            'graph_humidity': '',
            'graph_pressure': '',
            'day_from': day_from,
            'month_from': month_from,
            'year_from': year_from,
            'day_to': day_to,
            'month_to': month_to,
            'year_to': year_to,
        }
    else:
        context = {
            'station': station,
            'graph_temperature': graph_temperature,
            'graph_luminosity': graph_luminosity,
            'graph_humidity': graph_humidity,
            'graph_pressure': graph_pressure,
            'day_from': day_from,
            'month_from': month_from,
            'year_from': year_from,
            'day_to': day_to,
            'month_to': month_to,
            'year_to': year_to,
        }
    return render(request, 'weather_station/station_history.html', context)


def sobre(request):
    return render(request, 'weather_station/sobre.html')
