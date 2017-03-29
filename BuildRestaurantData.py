import requests
import sqlite3
import json
import config

conn=sqlite3.connect('restaurants_data.sqlite')
conn.text_factory = str
cur=conn.cursor()

cur.execute('''
	CREATE TABLE IF NOT EXISTS RESTAURANTS
	(res_id TEXT NOT NULL,
	res_name TEXT NOT NULL )
	''')

request_url = "https://developers.zomato.com/api/v2.1/search"


category_ids = [16,18,21,20,23,1,31,291,7,61,6,5,41,8,81]
start_index = 0

for category in category_ids:
	while(True):
		r = requests.get(request_url,headers={"user-key":config.API_KEY},params={"entity_id":1,"entity_type":"city","establishment_type":category,"start":start_index})
		js = json.loads(r.content)
		if start_index==js["results_found"] or start_index>=100 or js["results_shown"]==0:
			start_index=0
			break
		for i in range(0,js["results_shown"]):
			print js["restaurants"][i]["restaurant"]["name"] 
			 cur.execute('''
                     INSERT INTO RESTAURANTS (res_id,res_name) VALUES (?,?)''',(js["restaurants"][i]["restaurant"]["R"]["res_id"],js["restaurants"][i]["restaurant"]["name"] + ", " + js["restaurants"][i]["restaurant"]["location"]["locality"]))
			 conn.commit()


		start_index += js["results_shown"] 




