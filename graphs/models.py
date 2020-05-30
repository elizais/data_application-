from django.db import models

# Create your models here.
class Sensor(models.Model):
    location = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    characteristic = models.CharField(max_length=30)
    range_max = models.FloatField(default=150)
    range_min = models.FloatField(default=0)

    def __str__(self):
        return "%s %s %s" % (self.location, self.address, self.characteristic)

class Point(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='points')
    value = models.FloatField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return '%s' % self.value

