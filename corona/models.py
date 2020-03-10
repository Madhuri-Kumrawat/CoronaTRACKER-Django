from django.db import models
from django.db.models import Sum,QuerySet,Subquery,Count

# Create your models here.
class corona_data(models.Model):
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    confirmed=models.IntegerField(default=0)
    suspected=models.IntegerField(default=0)
    updated_at=models.DateTimeField('Updated Date',null=True)

    def all_countries(self):
        return corona_data.objects.all()

    def all_countries_confirmed(self):
        return corona_data.objects.values('country').annotate(total_cases=Sum('confirmed'))

