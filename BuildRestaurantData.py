import requests
import mysql.connector
import json
import config

conn=mysql.connector.connect(user='root',password='mysql',database='restaurants_data')
cur=conn.cursor()

sql = ("INSERT INTO restaurants "
               "(res_id,res_name) "
               "VALUES (%s, %s)")

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
			sql_data = (js["restaurants"][i]["restaurant"]["R"]["res_id"],js["restaurants"][i]["restaurant"]["name"] + ", " + js["restaurants"][i]["restaurant"]["location"]["locality"])
			cur.execute(sql,sql_data)
			conn.commit()


		start_index += js["results_shown"] 




