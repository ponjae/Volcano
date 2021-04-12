import folium
import pandas

data_frame = pandas.read_csv('Volcanoes_world.txt')
map = folium.Map(location=[55.723610, 13.205630],
                 zoom_start=4, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name='World volcanoes and other useful info')

lat = list(data_frame['Latitude'])
long = list(data_frame['Longitude'])
names = list(data_frame['Volcano Name'])
status = list(data_frame['Status'])
types = list(data_frame['Type'])
elev = list(data_frame['Elev'])


def color_producer(height):
    if height < 1500:
        return '#fa8f87'
    elif 1500 <= height < 3000:
        return '#ff1200'
    else:
        return '#851b13'


for lt, ln, name, el, status, ty in zip(lat, long, names, elev, status, types):
    fgv.add_child(folium.CircleMarker(location=[
        lt, ln], popup=f'This is the volcano: {name}, its height is {el}m. The type of the volcano is "{ty}" and its status is: {status}', fill_color=color_producer(el), radius=5, fill_opacity=0.8, fill=True, color=color_producer(el)))

fgv.add_child(folium.Marker(location=[
    55.723610, 13.205630], popup='This is where I currently live :)', icon=folium.Icon(color='green')))
fgv.add_child(folium.Marker(location=[
    40.453053, -3.688344], popup='This is where the best team in world plays', icon=folium.Icon(color='pink')))

fgj = folium.FeatureGroup(name='World population filter')

fgj.add_child(folium.GeoJson(
    data=open('world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                              else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgj)

map.add_child(folium.LayerControl())
map.save('index.html')
