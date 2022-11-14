from flask import Flask, render_template
import requests
import json
import mysql.connector

# Connect to database
mydb = mysql.connector.connect(
  host="awseb-e-bkyayhc2mq-stack-awsebrdsdatabase-xlcgvdroj3s0.ceajd2uuokj4.eu-west-1.rds.amazonaws.com",
  user="user",
  password="password",
  database="meteoapp"
)

# Temperature URL
temp_data_url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%22TLIST(M1)%22,%22C02431V02938%22%5D,%22dimension%22:%7B%22TLIST(M1)%22:%7B%22category%22:%7B%22index%22:%5B%22202209%22,%22202208%22,%22202207%22,%22202206%22,%22202205%22,%22202204%22,%22202203%22,%22202202%22,%22202201%22,%22202112%22,%22202111%22,%22202110%22%5D%7D%7D,%22C02431V02938%22:%7B%22category%22:%7B%22index%22:%5B%22007%22%5D%7D%7D%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22MTM02%22%7D,%22version%22:%222.0%22%7D%7D"

# Rainfall URL
rain_data_url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%22TLIST(M1)%22,%22C02431V02938%22%5D,%22dimension%22:%7B%22TLIST(M1)%22:%7B%22category%22:%7B%22index%22:%5B%22202209%22,%22202208%22,%22202207%22,%22202206%22,%22202205%22,%22202204%22,%22202203%22,%22202202%22,%22202201%22,%22202112%22,%22202111%22,%22202110%22%5D%7D%7D,%22C02431V02938%22:%7B%22category%22:%7B%22index%22:%5B%22007%22%5D%7D%7D%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22MTM01%22%7D,%22version%22:%222.0%22%7D%7D"

# Sun URL
sun_data_url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%22TLIST(M1)%22,%22C02431V02938%22%5D,%22dimension%22:%7B%22TLIST(M1)%22:%7B%22category%22:%7B%22index%22:%5B%22202209%22,%22202208%22,%22202207%22,%22202206%22,%22202205%22,%22202204%22,%22202203%22,%22202202%22,%22202201%22,%22202112%22,%22202111%22,%22202110%22%5D%7D%7D,%22C02431V02938%22:%7B%22category%22:%7B%22index%22:%5B%22007%22%5D%7D%7D%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22MTM03%22%7D,%22version%22:%222.0%22%7D%7D"

# Wind URL
wind_data_url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%22TLIST(M1)%22,%22C02431V02938%22%5D,%22dimension%22:%7B%22TLIST(M1)%22:%7B%22category%22:%7B%22index%22:%5B%22202209%22,%22202208%22,%22202207%22,%22202206%22,%22202205%22,%22202204%22,%22202203%22,%22202202%22,%22202201%22,%22202112%22,%22202111%22,%22202110%22%5D%7D%7D,%22C02431V02938%22:%7B%22category%22:%7B%22index%22:%5B%22007%22%5D%7D%7D%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22MTM04%22%7D,%22version%22:%222.0%22%7D%7D"

application = Flask(__name__)

def get_data(url):
   response = json.loads(requests.request("GET", url).text)
   data = response["result"]["value"]
   return data

@application.route("/")
def index():
   temp_data = get_data(temp_data_url)
   rain_data = get_data(rain_data_url)
   sun_data = get_data(sun_data_url)
   wind_data = get_data(wind_data_url)

   for i in range(len(wind_data)):
      wind_data[i] = round(1.852*wind_data[i], 1) # Convert knots to km/h

   mycursor = mydb.cursor()
   
   for i in range(12): # For each month update weather data
      sql_query = "UPDATE wether_data SET Avg_Max_Temp = %s, Avg_Min_Temp = %s, Mean_Temp = %s, Highest_Temp = %s, Lowest_Temp = %s, Total_Rain = %s, Most_Rain = %s, Raindays = %s, Total_Sun = %s, Most_Sun = %s, Max_Wind = %s WHERE Month_ID = '" + str(12-i) + "'"
      sql_values = (str(temp_data[0+i]), str(temp_data[12+i]), str(temp_data[24+i]), str(temp_data[36+i]), str(temp_data[48+i]), str(rain_data[0+i]), str(rain_data[12+i]), str(rain_data[24+i]), str(sun_data[0+i]), str(sun_data[12+i]), str(wind_data[0+i]))
      mycursor.execute(sql_query, sql_values)
   
   mydb.commit()

   return render_template("index.html", avg_max_temp_oct=temp_data[0],
                                        avg_max_temp_nov=temp_data[1],
                                        avg_max_temp_dec=temp_data[2],
                                        avg_max_temp_jan=temp_data[3],
                                        avg_max_temp_feb=temp_data[4],
                                        avg_max_temp_mar=temp_data[5],
                                        avg_max_temp_apr=temp_data[6],
                                        avg_max_temp_may=temp_data[7],
                                        avg_max_temp_jun=temp_data[8],
                                        avg_max_temp_jul=temp_data[9],
                                        avg_max_temp_aug=temp_data[10],
                                        avg_max_temp_sep=temp_data[11],
                                        avg_min_temp_oct=temp_data[12],
                                        avg_min_temp_nov=temp_data[13],
                                        avg_min_temp_dec=temp_data[14],
                                        avg_min_temp_jan=temp_data[15],
                                        avg_min_temp_feb=temp_data[16],
                                        avg_min_temp_mar=temp_data[17],
                                        avg_min_temp_apr=temp_data[18],
                                        avg_min_temp_may=temp_data[19],
                                        avg_min_temp_jun=temp_data[20],
                                        avg_min_temp_jul=temp_data[21],
                                        avg_min_temp_aug=temp_data[22],
                                        avg_min_temp_sep=temp_data[23],
                                        mean_temp_oct=temp_data[24],
                                        mean_temp_nov=temp_data[25],
                                        mean_temp_dec=temp_data[26],
                                        mean_temp_jan=temp_data[27],
                                        mean_temp_feb=temp_data[28],
                                        mean_temp_mar=temp_data[29],
                                        mean_temp_apr=temp_data[30],
                                        mean_temp_may=temp_data[31],
                                        mean_temp_jun=temp_data[32],
                                        mean_temp_jul=temp_data[33],
                                        mean_temp_aug=temp_data[34],
                                        mean_temp_sep=temp_data[35],
                                        high_temp_oct=temp_data[36],
                                        high_temp_nov=temp_data[37],
                                        high_temp_dec=temp_data[38],
                                        high_temp_jan=temp_data[39],
                                        high_temp_feb=temp_data[40],
                                        high_temp_mar=temp_data[41],
                                        high_temp_apr=temp_data[42],
                                        high_temp_may=temp_data[43],
                                        high_temp_jun=temp_data[44],
                                        high_temp_jul=temp_data[45],
                                        high_temp_aug=temp_data[46],
                                        high_temp_sep=temp_data[47],
                                        low_temp_oct=temp_data[48],
                                        low_temp_nov=temp_data[49],
                                        low_temp_dec=temp_data[50],
                                        low_temp_jan=temp_data[51],
                                        low_temp_feb=temp_data[52],
                                        low_temp_mar=temp_data[53],
                                        low_temp_apr=temp_data[54],
                                        low_temp_may=temp_data[55],
                                        low_temp_jun=temp_data[56],
                                        low_temp_jul=temp_data[57],
                                        low_temp_aug=temp_data[58],
                                        low_temp_sep=temp_data[59],
                                        total_rain_oct=rain_data[0],
                                        total_rain_nov=rain_data[1],
                                        total_rain_dec=rain_data[2],
                                        total_rain_jan=rain_data[3],
                                        total_rain_feb=rain_data[4],
                                        total_rain_mar=rain_data[5],
                                        total_rain_apr=rain_data[6],
                                        total_rain_may=rain_data[7],
                                        total_rain_jun=rain_data[8],
                                        total_rain_jul=rain_data[9],
                                        total_rain_aug=rain_data[10],
                                        total_rain_sep=rain_data[11],
                                        most_rain_oct=rain_data[12],
                                        most_rain_nov=rain_data[13],
                                        most_rain_dec=rain_data[14],
                                        most_rain_jan=rain_data[15],
                                        most_rain_feb=rain_data[16],
                                        most_rain_mar=rain_data[17],
                                        most_rain_apr=rain_data[18],
                                        most_rain_may=rain_data[19],
                                        most_rain_jun=rain_data[20],
                                        most_rain_jul=rain_data[21],
                                        most_rain_aug=rain_data[22],
                                        most_rain_sep=rain_data[23],
                                        raindays_oct=int(rain_data[24]),
                                        raindays_nov=int(rain_data[25]),
                                        raindays_dec=int(rain_data[26]),
                                        raindays_jan=int(rain_data[27]),
                                        raindays_feb=int(rain_data[28]),
                                        raindays_mar=int(rain_data[29]),
                                        raindays_apr=int(rain_data[30]),
                                        raindays_may=int(rain_data[31]),
                                        raindays_jun=int(rain_data[32]),
                                        raindays_jul=int(rain_data[33]),
                                        raindays_aug=int(rain_data[34]),
                                        raindays_sep=int(rain_data[35]),
                                        total_sun_oct=sun_data[0],
                                        total_sun_nov=sun_data[1],
                                        total_sun_dec=sun_data[2],
                                        total_sun_jan=sun_data[3],
                                        total_sun_feb=sun_data[4],
                                        total_sun_mar=sun_data[5],
                                        total_sun_apr=sun_data[6],
                                        total_sun_may=sun_data[7],
                                        total_sun_jun=sun_data[8],
                                        total_sun_jul=sun_data[9],
                                        total_sun_aug=sun_data[10],
                                        total_sun_sep=sun_data[11],
                                        most_sun_oct=sun_data[12],
                                        most_sun_nov=sun_data[13],
                                        most_sun_dec=sun_data[14],
                                        most_sun_jan=sun_data[15],
                                        most_sun_feb=sun_data[16],
                                        most_sun_mar=sun_data[17],
                                        most_sun_apr=sun_data[18],
                                        most_sun_may=sun_data[19],
                                        most_sun_jun=sun_data[20],
                                        most_sun_jul=sun_data[21],
                                        most_sun_aug=sun_data[22],
                                        most_sun_sep=sun_data[23],
                                        max_wind_oct=wind_data[0],
                                        max_wind_nov=wind_data[1],
                                        max_wind_dec=wind_data[2],
                                        max_wind_jan=wind_data[3],
                                        max_wind_feb=wind_data[4],
                                        max_wind_mar=wind_data[5],
                                        max_wind_apr=wind_data[6],
                                        max_wind_may=wind_data[7],
                                        max_wind_jun=wind_data[8],
                                        max_wind_jul=wind_data[9],
                                        max_wind_aug=wind_data[10],
                                        max_wind_sep=wind_data[11])

if __name__ == "__main__":
   application.run()
