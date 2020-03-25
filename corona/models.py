from django.db import models
from django.db.models import Sum,QuerySet,Subquery,Count

# Create your models here.
from django.db.models.functions import TruncDate, TruncMonth, Trunc


class country(models.Model):
    city=models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100)
    lat=models.DecimalField(max_length=100,decimal_places=4,max_digits=7)
    lng=models.DecimalField(max_length=100,decimal_places=4,max_digits=7)

class country_total_data(models.Model):
    Date=models.DateTimeField('Added Date',null=True)
    Country=models.CharField(max_length=100)
    Confirmed=models.IntegerField(default=0)
    Recovered=models.IntegerField(default=0)
    Deaths=models.IntegerField(default=0)


class corona_data(models.Model):
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    confirmed=models.IntegerField(default=0)
    recovered=models.IntegerField(default=0)
    deaths=models.IntegerField(default=0)
    updated_at=models.DateTimeField('Updated Date',null=True)
    lat = models.DecimalField(max_length=100, decimal_places=4, max_digits=7)
    lng = models.DecimalField(max_length=100, decimal_places=4, max_digits=7)

    def all_countries(self):
        return country.objects.all()

    def total_countries_confirmed(self,country_name):
        if country_name:
            return corona_data.objects.all().filter(country=country_name).aggregate(total_cases=Sum('confirmed'))
        else:
            return corona_data.objects.all().aggregate(total_cases=Sum('confirmed'))

    def total_countries_deaths(self,country_name):
        if country_name:
            return corona_data.objects.all().filter(country=country_name).aggregate(total_cases=Sum('deaths'))
        else:
            return corona_data.objects.all().aggregate(total_cases=Sum('deaths'))

    def total_countries_recovery(self,country_name):
        if country_name:
            return corona_data.objects.all().filter(country=country_name).aggregate(total_cases=Sum('recovered'))
        else:
            return corona_data.objects.all().aggregate(total_cases=Sum('recovered'))

    def all_countries_confirmed(self,country_name):
        total_Cases= corona_data.objects.values('country').annotate(total_cases=Sum('confirmed'))
        if country_name:
            total_Cases=total_Cases.filter(country=country_name)
        return total_Cases

    def map_data(self):
        return corona_data.objects.raw('SELECT corona_corona_data.id, corona_corona_data.country,corona_corona_data.state,corona_country.lat,corona_country.lng,sum(confirmed) as total_cases '
                                       ' FROM corona_corona_data '
                                       ' JOIN corona_country ON corona_corona_data.country=corona_country.country AND corona_corona_data.state=corona_country.state'
                                       ' GROUP BY corona_corona_data.country,corona_corona_data.state'                                       
                                       ' HAVING sum(confirmed)>0')

    def monthly_data(self):
        return corona_data.objects.raw('SELECT corona_corona_data.id, sum(confirmed) as total_cases'
                                       ' FROM corona_corona_data '
                                       ' GROUP BY DATE_FORMAT(corona_corona_data.updated_at, "%Y-%m") as month_Dates'                                       
                                       ' HAVING sum(confirmed)>0')



