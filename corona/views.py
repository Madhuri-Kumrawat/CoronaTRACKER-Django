from django.http import HttpResponse
from django.views import generic
from .models import corona_data
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py
import plotly.express as px
import pprint

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
        # df = px.data.gapminder().query("year == 2007")
        # fig = px.scatter_geo(df, locations="iso_alpha",
        #                      size="pop",  # size of markers, "pop" is one of the columns of gapminder
        #                      )
        limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]
        colors = ["rgb(0,116,217)", "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "lightgrey"]
        cities = []
        scale = 500
        maps_data=corona_data.map_data(self)
        for data in maps_data:
            country_raw_text = '{0}'.format(data.total_cases) +' <br> '+data.state + '<br> ' + (data.country )

            city = go.Scattergeo(
                locationmode='country names',
                lon=[data.lng],
                lat=[data.lat],
                text=country_raw_text,
                marker=go.scattergeo.Marker(
                    size=data.total_cases / scale,
                    color=colors[3],
                    line=go.scattergeo.marker.Line(
                        width=0.5, color='rgb(40,40,40)'
                    ),
                    sizemode='area'
                ),
                name='{0}'.format(data.total_cases))
            cities.append(city)

        layout = go.Layout(
            title=go.layout.Title(
                text='Corona Effect'
            ),
            showlegend=True,
            geo=go.layout.Geo(
                scope='world',
                projection=go.layout.geo.Projection(
                    type='natural earth'
                ),
                showland=True,
                landcolor='rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)"
            )
        )

        fig = go.Figure(data=cities, layout=layout)
        return py.plot(fig, filename='bubble_map',auto_open=False,sharing='public')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Corona Details'

        context['maps_data'] =corona_data.map_data(self)

        return context


class DetailView(generic.DetailView):
    template_name = 'corona/detail.html'
    context_object_name='country_detail'

    def get_object(self):
        object = corona_data.objects.filter(country=self.kwargs['country']).first()
        return object

