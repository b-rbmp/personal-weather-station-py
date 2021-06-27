from django.db import models

# Create your models here.
# Weather Station identified with a 20-digit apikey. Should be used for validation. Not worried about encryption since its a private
# weather station, but should be handled if used by the public
class WeatherStation(models.Model):
    api_key = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    @property
    def last_record(self):
        "Returns the last weather record."
        return self.weatherrecord_set.latest('record_date')

    def __str__(self):
        return self.name
    

class WeatherRecord(models.Model):
    record_date = models.DateTimeField('momento de publicacao')
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    humidity = models.DecimalField(max_digits=6, decimal_places=2)
    light = models.DecimalField(max_digits=6, decimal_places=2)
    pressure = models.DecimalField(max_digits=6, decimal_places=2)
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)

    def __str__(self):
        return self.record_date.strftime("%m/%d/%Y-%H:%M:%S") + ' : T='+str(self.temperature)+' °C | H='+ str(self.humidity)+'% | I=' + str(self.light) + ' lux | P=' + str(self.pressure) + ' hPa'

    class Meta:
            ordering = ['-record_date']