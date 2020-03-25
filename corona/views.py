from django.db import connection
from django.http import HttpResponse, request, JsonResponse
from django.template.context_processors import csrf
from django.views import generic
from flask import jsonify

from .models import corona_data, country
import plotly
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py
import plotly.express as px
import random

from django.shortcuts import get_object_or_404

# Create your views here.
def change_country_data(request):
    centre_countries = dict()
    country_param = ''
    if request.GET.get('country',None):
        country_param = request.GET.get('country',None)
        country_data=country.objects.filter(country=country_param)[0]
        centre_countries['lon'] = country_data.lng
        centre_countries['lat'] = country_data.lat
    else:
        country_param = '';
    limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]
    colors = ["rgb(0,116,217)", "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "red"]
    cities = []
    countries_taken = []
    scale = 50
    country_colors = {}
    maps_data = corona_data.map_data(request)
    for data in maps_data:
        country_raw_text = '{0}'.format(data.total_cases) + ' <br> ' + data.state + '<br> ' + (data.country)
        list_index = '';
        list_entry = False
        if data.country in countries_taken:
            list_index = ''
            list_entry = False
        else:
            list_index = '{0}'.format(data.country)
            countries_taken.append(data.country)
            country_colors[data.country] = colors[random.randint(0, 4)]
            list_entry = True

        city = go.Scattergeo(
            locationmode='country names',
            lon=[data.lng],
            lat=[data.lat],
            text=country_raw_text,
            marker=go.scattergeo.Marker(
                size=10,
                color=country_colors[data.country],
                line=go.scattergeo.marker.Line(
                    width=0.5, color='rgb(40,40,40)'
                ),
                sizemode='area'
            ),
            name=list_index,
            showlegend=list_entry,
        )
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
            showcountries=True,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            center=dict(centre_countries)
        ),
        height=300, margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    fig = go.Figure(data=cities, layout=layout)

    output_data_total_confirmed = corona_data.total_countries_confirmed(request, country_param)
    output_data_total_deaths = corona_data.total_countries_deaths(request, country_param)
    output_data_total_recovered = corona_data.total_countries_recovery(request, country_param)

    return JsonResponse({'data':(plotly.offline.plot(fig, filename='bubble_map', auto_open=False, output_type='div')),
                         'total_confirmed':output_data_total_confirmed['total_cases'],
                         'total_deaths': output_data_total_deaths['total_cases'],
                         'total_recovered': output_data_total_recovered['total_cases']
                         }, status = 200)


class IndexView(generic.ListView):
    template_name = 'corona/index.html'
    context_object_name = 'country_wise_cases'

    def get_queryset(self):
        if self.kwargs.items() :
            country_param =self.kwargs['country']
        else:
            country_param ='';
        limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]
        colors = ["rgb(0,116,217)", "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "red"]
        cities = []
        countries_taken=[]
        scale = 50
        country_cases=corona_data.all_countries_confirmed(self,'')
        country_colors={}
        maps_data=corona_data.map_data(self)
        for data in maps_data:
            country_raw_text = '{0}'.format(data.total_cases) +' <br> '+data.state + '<br> ' + (data.country )
            list_index='';
            list_entry=False
            if data.country in countries_taken:
                list_index=''
                list_entry=False
            else:
                list_index='{0}'.format(data.country)
                countries_taken.append(data.country)
                country_colors[data.country]=colors[random.randint(0,4)]
                list_entry=True

            city = go.Scattergeo(
                locationmode='country names',
                lon=[data.lng],
                lat=[data.lat],
                text=country_raw_text,
                marker=go.scattergeo.Marker(
                    size=10,
                    color=country_colors[data.country],
                    line=go.scattergeo.marker.Line(
                        width=0.5, color='rgb(40,40,40)'
                    ),
                    sizemode='area'
                ),
                name=list_index,
                showlegend=list_entry,
                )
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
                showcountries=True,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)",

            ),
            paper_bgcolor="#222a42",
            plot_bgcolor="#222a42",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        fig = go.Figure(data=cities, layout=layout)
        return plotly.offline.plot(fig, filename='bubble_map', auto_open=False, output_type='div')
            #return py.plot(fig, filename='bubble_map',auto_open=False,sharing='public')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Corona Details'

        ###################### Total cases in Table Format #######################
        context['maps_data'] =corona_data.all_countries_confirmed(self,'')

        ################## Line Chart DAta #####################
        cursor = connection.cursor()
        query = 'SELECT corona_corona_data.id, sum(confirmed) as total_cases, DATE_FORMAT(corona_corona_data.updated_at, "%M, %y") as month_name FROM corona_corona_data  GROUP BY DATE_FORMAT(corona_corona_data.updated_at, "%Y-%m") HAVING sum(confirmed)>0';
        cursor.execute(query)
        context['month_data']=month_data=cursor.fetchall()
        context['csrf_req']=csrf(request);
        x_arr=[]
        y_arr=[]
        for ri in month_data:
            x_arr.append(ri[2])
            y_arr.append(ri[1])

        fig = go.Figure(data=go.Scatter(
                x=x_arr,
                y=y_arr
            ))
        fig.update_layout(paper_bgcolor="#222a42",
            plot_bgcolor="#222a42")
        context['month_wise_data'] =  plotly.offline.plot(fig, filename='line_map', auto_open=False, output_type='div')

        ######### Total deaths #################

        context['total_confirmed'] = corona_data.total_countries_confirmed(self,'')
        context['total_deaths'] = corona_data.total_countries_deaths(self, '')
        context['total_recovered'] = corona_data.total_countries_recovery(self, '')

        return context


class DetailView(generic.DetailView):
    template_name = 'corona/detail.html'
    context_object_name='country_detail'

    def get_object(self):
        object = corona_data.objects.filter(country=self.kwargs['country']).first()
        return object

