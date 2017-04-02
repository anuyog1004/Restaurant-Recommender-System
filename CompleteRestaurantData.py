import requests
import mysql.connector
import json
import config

conn=mysql.connector.connect(user='root',password='mysql',database='restaurants_data')
cur=conn.cursor(buffered=True)
cursor=conn.cursor(buffered=True)

request_url = "https://developers.zomato.com/api/v2.1/restaurant?res_id="

query = ("SELECT res_id,res_name FROM restaurants")
sql = ("INSERT INTO restaurants_complete "
        "(res_id, res_name, res_url) "
        "VALUES (%s, %s, %s)")

cur.execute(query)

for (res_id,res_name) in cur:
	r = requests.get(request_url + res_id,headers={"user-key":config.API_KEY})
	js = json.loads(r.content)
	sql_data = (res_id,res_name,js["url"])
	cursor.execute(sql,sql_data)
	conn.commit()

cur.close()
cursor.close()
conn.close()