import folium
from folium import plugins
import numpy as np
import pandas as pd
import json
from cloudant import CouchDB
from shapely.geometry import shape, Point
from folium.plugins import FloatImage
import sys

endpoint = {
    'trump_pos': 'twitter/_design/trump/_view/trumppositive?reduce=false',
    'trump_neg': 'twitter/_design/trump/_view/trumpnegative?reduce=false',
    'android': 'twitter/_design/phonebrand/_view/android?reduce=false',
    'iphone': 'twitter/_design/phonebrand/_view/iphone?reduce=false',
    'jobseeker_neg': 'twitter/_design/jobseeker/_view/keywordsnegative?reduce=false',
    'jobseeker_pos': 'twitter/_design/jobseeker/_view/keywordspositive?reduce=false',
    'sentiment_neg': 'twitter/_design/depression/_view/negativesentiment?reduce=false',
    'sentiment_neu': 'twitter/_design/depression/_view/neutralsentiment?reduce=false',
    'sentiment_pos': 'twitter/_design/depression/_view/positivesentiment?reduce=false'
}

scenario_path = 'AURIN/LGA_composite_small.json'

ip_address = sys.argv[1]

# ip_address = '172.26.129.225'

# Request view from CouchDB
def get_view(endpoint):

    client = CouchDB('admin', 'admin', url = 'http://' + ip_address +':5984', connect = True, auto_renew = True)
    end_point = '{0}/{1}'.format(client.server_url, endpoint)
    response = client.r_session.get(end_point)

    return response.json()


# Extract coordinates and convert to proper format

def coordinates_processing(view):
    
    def get_center(bounding_box):

        x, y = 0, 0

        for corner in bounding_box:
            x += corner[0]
            y += corner[1]

        return [x / 4, y / 4]
    
    coordinates, points = list(), list()

    for coordinate in view['rows']:

        center = get_center(coordinate['key'][0][0])
        coordinates.append(center)
        points.append(Point(center))

    for pair in coordinates:
        pair[0], pair[1] = pair[1], pair[0]

    return np.asarray(coordinates), points


coord_array_trump_pos, points_trump_pos = coordinates_processing(get_view(endpoint['trump_pos']))
coord_array_trump_neg, points_trump_neg = coordinates_processing(get_view(endpoint['trump_neg']))

coord_array_jobseeker_pos, points_jobseeker_pos = coordinates_processing(get_view(endpoint['jobseeker_pos']))
coord_array_jobseeker_neg, points_jobseeker_neg = coordinates_processing(get_view(endpoint['jobseeker_neg']))

coord_array_android, points_android = coordinates_processing(get_view(endpoint['android']))
coord_array_iphone, points_iphone = coordinates_processing(get_view(endpoint['iphone']))

coord_array_sentiment_neg, points_sentiment_neg = coordinates_processing(get_view(endpoint['sentiment_neg']))
coord_array_sentiment_neu, points_sentiment_neu = coordinates_processing(get_view(endpoint['sentiment_neu']))
coord_array_sentiment_pos, points_sentiment_pos = coordinates_processing(get_view(endpoint['sentiment_pos']))


with open(scenario_path, 'r') as file:
    aurin_data = json.load(file)


# Tweet aggregation based on area

def tweet_count_area_aggregation(aurin_data, points, new_prop_name):
    
    for feature in aurin_data['features']:
        count = 0
        polygon = shape(feature['geometry']).buffer(0)

        for point in points:
            if polygon.contains(point):
                count += 1

        feature['properties'][new_prop_name] = count

tweet_count_area_aggregation(aurin_data, points_android, 'android_tc')
tweet_count_area_aggregation(aurin_data, points_iphone, 'iphone_tc')

tweet_count_area_aggregation(aurin_data, points_trump_pos, 'trump_pos_tc')
tweet_count_area_aggregation(aurin_data, points_trump_neg, 'trump_neg_tc')

tweet_count_area_aggregation(aurin_data, points_jobseeker_pos, 'jobseeker_pos_tc')
tweet_count_area_aggregation(aurin_data, points_jobseeker_neg, 'jobseeker_neg_tc')

tweet_count_area_aggregation(aurin_data, points_sentiment_neg, 'sentiment_neg_tc')
tweet_count_area_aggregation(aurin_data, points_sentiment_neu, 'sentiment_neu_tc')
tweet_count_area_aggregation(aurin_data, points_sentiment_pos, 'sentiment_pos_tc')


# Calculating various metrics

for feature in aurin_data['features']:
    
    p = feature['properties']
    
    # Wealth metric
    
    lower = (p['hi_1_149_tot'] + p['hi_150_299_tot'] + p['hi_300_399_tot'] + p['hi_400_499_tot'] + p['hi_500_649_tot'] + p['hi_650_799_tot']) / p['tot_tot']
    upper = (p['hi_2500_2999_tot'] + p['hi_3000_3499_tot'] + p['hi_3500_3999_tot'] + p['hi_4000_more_tot']) / p['tot_tot']
    
    p['wealth'] = (upper - lower) * (upper + lower)
    
    # Mental metric
    
    mental = p['M0_admis_mental_hlth_rltd_cond_p_all_hosps_2016_17_asr_100k']
    mood = p['M0_admis_mood_affective_disorders_p_all_hosps_2016_17_asr_100k']
    
    if not mental:
        mental = 0    
    if not mood:
        mood = 0
    
    p['mental_health'] = mental + mood
    
    # Unemployment
    
    p['unemployment'] = p['M0_unemployment_rate_perc']
    
    # IRSD
    
    p['irsd'] = p['M0_index_of_relative_socio_economic_disadv_irsd']


# Extract properties for different area

properties = list()

for i in aurin_data['features']:
    properties.append(i['properties'])
    
df_properties = pd.DataFrame.from_dict(properties)


# Map object creation with folium

m1 = folium.Map(location = [-37.8136, 144.9631], zoom_start = 8)
m2 = folium.Map(location = [-37.8136, 144.9631], zoom_start = 8)
m3 = folium.Map(location = [-37.8136, 144.9631], zoom_start = 8)


# Adding layers to the map

def plot_choropleth(m, layer_name, target_column):
    
    folium.Choropleth(
        geo_data = aurin_data,
        name = layer_name,
        data = df_properties,
        columns = ['lga_code_2016', target_column],
        key_on = 'feature.properties.lga_code_2016',
        fill_color = 'YlGn',
        fill_opacity = 0.7,
        line_opacity = 0.2,
    ).add_to(m)
    
plot_choropleth(m1, 'IRSD Choropleth', 'irsd')
plot_choropleth(m2, 'Wealth Metric Choropleth', 'wealth')
plot_choropleth(m3, 'Mental Health Choropleth', 'mental_health')

def plot_popup(m, fields, aliases):

    folium.features.GeoJson(
        
        aurin_data,
        name = 'Tweet Statistics Popup',
        popup = folium.GeoJsonPopup(
            fields = fields, 
            aliases = aliases
        ),
        style_function = lambda style: {'fillColor': '#00000000', 'color': '#00000000'}

    ).add_to(m)

plot_popup(m1, ['jobseeker_pos_tc', 'jobseeker_neg_tc'], ['Positive opinion on Employment:', 'Negative opinion on Employment:'])
plot_popup(m2, ['iphone_tc', 'android_tc'], ['Tweets from iOS:', 'Tweets from Android:'])
plot_popup(m3, ['sentiment_pos_tc', 'sentiment_neu_tc', 'sentiment_neg_tc'], ['Positive Tweets:', 'Neutral Tweets:', 'Negative Tweets:'])

def plot_heatmap(m, coord_array, layer_name):

    plugins.HeatMap(
        coord_array, 
        name = layer_name, 
        radius = 10
    ).add_to(m)
    
plot_heatmap(m1, coord_array_jobseeker_pos, 'Positive on Jobseeker Heatmap')
plot_heatmap(m1, coord_array_jobseeker_neg, 'Negative on Jobseeker Heatmap')

plot_heatmap(m2, coord_array_android, 'Android Tweet Heatmap')
plot_heatmap(m2, coord_array_iphone, 'IOS Tweet Heatmap')

plot_heatmap(m3, coord_array_sentiment_pos, 'Positive Tweet Heatmap')
plot_heatmap(m3, coord_array_sentiment_neu, 'Neutral Tweet Heatmap')
plot_heatmap(m3, coord_array_sentiment_neg, 'Negative Tweet Heatmap')

def plot_float_analysis(m, image_file):

    FloatImage(image_file, bottom=0, left=0).add_to(m)

plot_float_analysis(m1, 'image/irsd.png')
plot_float_analysis(m2, 'image/wealth.png')
plot_float_analysis(m3, 'image/mental.png')

folium.LayerControl().add_to(m1)
folium.LayerControl().add_to(m2)
folium.LayerControl().add_to(m3)

m1.save('map1.html')
m2.save('map2.html')
m3.save('map3.html')


# Some customized html component to be added

NAVBAR_HTML = '''
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
        <li><a href="#">Home</a href="/map1.html"></li>
        <li><a href="#">Scenario 1</a href="/map1.html"></li>
        <li><a href="#">Scenario 2</a href="/map2.html"></li>
        <li><a href="#">Scenario 3</a href="/map3.html"></li>
      </ul>
    </div>
  </div>
</nav>
'''

HEATMAP_ADJUST = '<style>.leaflet-heatmap-layer{z-index:300 !important}</style>'


# Postprocessing to the html

def postprocessing(html_file):
    
    with open(html_file, 'r') as file_in:
        map_html = file_in.read()

    map_html = map_html.replace('<body>', '<body>' + NAVBAR_HTML) + HEATMAP_ADJUST

    with open(html_file, 'w') as file_out:
        file_out.write(map_html)
        
postprocessing('map1.html')
postprocessing('map2.html')
postprocessing('map3.html')