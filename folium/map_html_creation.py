import folium
from folium import plugins
import numpy as np
import pandas as pd
import json
from cloudant import CouchDB

NAVBAR = '''
<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">City Analytics</a>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
        <li><a href="#">Scenario 1</a href="/index.html"></li>
        <li><a href="#">Scenario 2</a></li>
        <li><a href="#">Scenario 3</a></li>
        <li><a href="#">Scenario 4</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="#"><span class="glyphicon glyphicon-log-in"></span> Login</a></li>
      </ul>
    </div>
  </div>
</nav>
'''

# Request view from CouchDB
client = CouchDB('admin','admin',url='http://172.26.129.225:5984', connect=True, auto_renew=True)
end_point = '{0}/{1}'.format(client.server_url, 'twitter/_design/trump/_view/trumpnegative?reduce=false')
response = client.r_session.get(end_point)

view = response.json()

# Extract coordinates and convert to proper format
coordinates = list()

for coordinate in view['rows']:
    coordinates.append(coordinate['key'][0][0][0])

for pair in coordinates:
    pair[0], pair[1] = pair[1], pair[0]

coordinate_array = np.asarray(coordinates)

# Create map html with coordinate data
m = folium.Map(location = [-37.8136, 144.9631], zoom_start=5)

plugins.HeatMap(coordinate_array, radius=30).add_to(m)
folium.LayerControl().add_to(m)

m.save('map.html')

# Add navigation bar to the html
with open('map.html', 'r') as file_in:
    map_html = file_in.read()

map_html = map_html.replace('<body>', '<body>' + NAVBAR)

with open('map_with_nav.html', 'w') as file_out:
    file_out.write(map_html)