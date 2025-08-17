from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import pandas
from geopy.distance import geodesic

NETWORK_URL = "https://api.citybik.es/v2/networks/bikesampa"

def clean_stations(data):
    stations = []
    for station in data['network']['stations']:
        station_data = {}
        for key in station.keys():
            if key != 'extra':
                station_data[key] = station[key]
            else:
                for extra_key in station['extra'].keys():
                    station_data[extra_key] = station['extra'][extra_key]
        stations.append(station_data)
    
    return pandas.DataFrame(stations)

def get_distances(data):
    supersim_lat = -23.556641
    supersim_lng = -46.681632
    distances = []
    for station in data['network']['stations']:
        lat = station['latitude']
        lng = station['longitude']
        p1 = (lat, lng)
        p2 = (supersim_lat, supersim_lng)
        distance = geodesic(p1, p2).km
        distances.append(distance)
    return distances

def get_and_insert_data():
    response = requests.get(NETWORK_URL)
    data = response.json()

    df_stations = clean_stations(data)
    df_stations['distance_to_supersim'] = get_distances(data)

    conn = psycopg2.connect(
        dbname="citybik",
        user="postgres",
        password="postgres",
        host="postgres",
        port="5432"
    )
    cur = conn.cursor()

    # Insert row by row
    insert_query = """
        INSERT INTO public.citybik_log (id, updated_at, station_name, free_bikes, empty_slots, address, distance_to_supersim, renting, "returning", has_ebikes, ebikes, normal_bikes, payment_terminal)
        VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """

    for _, row in df_stations[['id','name','free_bikes','empty_slots','address','distance_to_supersim','renting','returning','has_ebikes','ebikes','normal_bikes','payment-terminal']].iterrows():
        cur.execute(insert_query, tuple(row))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id = "citybikes_monitoring",
    start_date=datetime(2025, 8, 17),
    schedule_interval="*/5 * * * *",
    tags = ['API','Postgres'],
    catchup = False
) as dag:

    get_and_insert_task = PythonOperator(
        task_id="get_and_insert_task",
        python_callable=get_and_insert_data,
    )
