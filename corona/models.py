from django.db import models
from django.db.models import Sum,QuerySet,Subquery,Count

# Create your models here.
class country(models.Model):
    city=models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100)
    lat=models.DecimalField(max_length=100,decimal_places=4,max_digits=7)
    lng=models.DecimalField(max_length=100,decimal_places=4,max_digits=7)

class corona_data(models.Model):
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    confirmed=models.IntegerField(default=0)
    suspected=models.IntegerField(default=0)
    updated_at=models.DateTimeField('Updated Date',null=True)

    def all_countries(self):
        return country.objects.all()

    def all_countries_confirmed(self):
        return corona_data.objects.values('country').annotate(total_cases=Sum('confirmed'))
    def map_data(self):
        return corona_data.objects.raw('SELECT corona_corona_data.id, corona_corona_data.country,corona_corona_data.state,corona_country.lat,corona_country.lng,sum(confirmed) as total_cases  FROM corona_corona_data '
                                       ' JOIN corona_country ON corona_corona_data.country=corona_country.country AND corona_corona_data.state=corona_country.state'
                                       ' GROUP BY corona_corona_data.country,corona_corona_data.state'
                                       ' HAVING sum(confirmed)>0')
