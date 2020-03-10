from django.http import HttpResponse
from django.views import generic
from .models import corona_data
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py
import plotly.express as px

from django.shortcuts import get_object_or_404

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'corona/index.html'
    context_object_name = 'country_wise_cases'

    def get_queryset(self):
        # trace0 = go.Scatter(
        #     x=[1, 2, 3, 4],
        #     y=[10, 15, 13, 17]
        # )
        # trace1 = go.Scatter(
        #     x=[1, 2, 3, 4],
        #     y=[16, 5, 11, 9]
        # )
        # data = [trace0, trace1]
        df = px.data.gapminder().query("year == 2007")
        fig = px.scatter_geo(df, locations="iso_alpha",
                             size="pop",  # size of markers, "pop" is one of the columns of gapminder
                             )
        return py.plot(fig, filename='bubble_map',auto_open=False,sharing='public')

class DetailView(generic.DetailView):
    template_name = 'corona/detail.html'
    context_object_name='country_detail'

    def get_object(self):
        object = corona_data.objects.filter(country=self.kwargs['country']).first()
        return object

