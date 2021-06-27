from django.contrib import admin

from .models import WeatherRecord, WeatherStation

# Register your models here.
class WeatherRecordAdmin(admin.ModelAdmin):
    fields = ('station', 'record_date', 'temperature', 'humidity', 'light', 'pressure')

class WeatherStationAdmin(admin.ModelAdmin):
    fields = ('name', 'api_key', ('city', 'country'))

admin.site.register(WeatherRecord, WeatherRecordAdmin)
admin.site.register(WeatherStation, WeatherStationAdmin)

