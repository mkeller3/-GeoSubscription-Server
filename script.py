import time
import requests
import json
import os
import psycopg2
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from flask import Flask

app = Flask(__name__)
logging.basicConfig()

geo_subscription_information = {
    'subscription_name': 'test',
    'input_connector': 'arcgis',
    'input_url': 'https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Forecasts_Guidance_Warnings/watch_warn_adv/MapServer/1',
    'table_id': 'geo_test',
    'intersect_table_id': 'geo_intersect',
    'filters':{
        'attribute_filters':[{
            'prod_type': 'High Wind Warning',
            'where_clause': '=',
            'operator': 'OR'
        },{
            'prod_type': 'Flood Watch',
            'where_clause': '='
        }]
    },
    'builders':{
        'intersect':{
            'table':'test_points_2'
        }
    }
}

postgresHost = 'localhost'
postgresDatabase = 'gisdata'
postgresUser = 'postgres'
postgresPassword = ''


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    if geo_subscription_information['input_connector'] == 'arcgis':
        url = geo_subscription_information['input_url']+"/query?outFields=*&returnGeometry=true&f=geojson"
        where_clause = '&where='
        attribute_filter_count = len(geo_subscription_information['filters']['attribute_filters'])
        attribute_counter = 1
        for filter_clause in geo_subscription_information['filters']['attribute_filters']:
            for key, value in filter_clause.iteritems():
                if key == 'where_clause':
                    where_operator = value                    
                elif key == 'operator':
                    operator = value
                else:
                    column = key
                    attribute_value = value
            if attribute_counter < attribute_filter_count:
                where_clause = where_clause + column + where_operator + "'" + attribute_value + "' "+operator+" "
            else:
                where_clause = where_clause + column + where_operator + "'" + attribute_value + "'"
            attribute_counter = attribute_counter + 1
        url = url + where_clause
        print url
        resp = requests.get(url=url)
        data = resp.json() 
        with open(geo_subscription_information['table_id']+'.geojson', 'w') as outfile:  
            json.dump(data, outfile)
        os.system('ogr2ogr -f "PostgreSQL" PG:"host='+postgresHost+' user='+postgresUser+' dbname='+postgresDatabase+' password='+postgresPassword+'" '+geo_subscription_information['table_id']+'.geojson -nln '+geo_subscription_information['table_id']+' -lco GEOMETRY_NAME=geom -overwrite')
        #conn = psycopg2.connect("host="+postgresHost+" dbname="+postgresDatabase+" user="+postgresUser+" password="+postgresHost)
        conn = psycopg2.connect("host=localhost dbname=gisdata user=postgres password=")
        cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS '+geo_subscription_information['intersect_table_id']+';')
        cur.execute("create table "+geo_subscription_information['intersect_table_id']+" as select test_points_2.geom from test_points_2,"+geo_subscription_information['table_id']+" where st_intersects("+geo_subscription_information['table_id']+".geom,test_points_2.geom)")
        cur.execute("select COUNT(*) from test_points_2,"+geo_subscription_information['table_id']+" where st_intersects("+geo_subscription_information['table_id']+".geom,test_points_2.geom)")
        count = cur.fetchone()
        conn.commit()
        cursor.close()
        conn.close()   
        print count[0]
    print 'success'
    


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
scheduler.start()


if __name__ == '__main__':
    app.run()