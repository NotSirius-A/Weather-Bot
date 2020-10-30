#!/usr/bin/python3

import requests
import smtplib
import ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


#******  Config  ******************************************

#look up the tutorial for the server you're using, type in google
#something like "SMTP_SERVER smtp settings" 

port = 587 #**SMTP_PORT**  
smtp_server = "**SMTP_SERVER**"
sender_email = "**SENDER_EMAIL**"
password = "**SMTP_PASSOWORD**"

receiver_list_path = "**PATH_TO_JSON**" + "receiver_list.json"

log = True
log_path = "**PATH_WHERE_TO_STORE_LOGS**" + "weather_bot_log.txt"

url = "http://api.openweathermap.org/data/2.5/onecall"
#you have to register an account on their website, after few minutes theyll email you the key
api_key = "*** Open Weather API Key ***"

#this will change the languague ONLY of the "State" section, just leave it if you want english
#if you want to translate the whole email, youll need to hardcode it [in the make_message()], there's no other way.
lang = "en" 

#**********************************************************



def main():
    message = MIMEMultipart('alternative')

    receivers = []
    with open(receiver_list_path) as f:
        receivers = json.load(f)

    for user in receivers:
        data = get_weather_data(url=url, key=api_key, lat=user['coord'][0], lon=user['coord'][1])
  
        message = make_message(user, data)

        message['From'] = sender_email
        message['To'] = user['adress']

        send_email(sender_email, user['adress'], message, time.ctime(data['current']['dt']))

    exit()



def get_weather_data(url, key, lat, lon):
    #Open weather api works by sending a simple get request with some url parameters
    url = url + "?lat=" + str(lat) + "&lon=" + str(lon) +"&appid=" + str(key) + "&exclude=minutely,daily,alerts&units=metric&lang=" + str(lang)
    return requests.get(url).json()

def make_message(receiver, data):
    #if you want to understand the forecast[] list, you need to know how the API response looks like

    message = MIMEMultipart('alternative')

    time_of_req = data['current']['dt']
    message['Subject'] = f"Weather bot: {time.ctime(time_of_req)[4:10]}"

    coords = f"Latitude = {data['lat']} Longtitude = {data['lon']}"
  
    forecast = []
    i = 0

    #this loop gathers all data and orginizes it (nested list/dict)
    for hours_in_future in receiver['forecasts']:
        forecast.append({})

        if hours_in_future == 0:
            forecast[0]['time'] = time.ctime(time_of_req)
            forecast[0]['state'] = data['current']['weather'][0]['description']
            forecast[0]['temp'] = int(data['current']['temp'])
            forecast[0]['humidity'] = data['current']['humidity']    
            forecast[0]['icon'] = data['current']['weather'][0]['icon']        
        else:
            #basically add how many hours as specified in the recievers{}
            forecast[i]['time'] = time.ctime(time_of_req + hours_in_future*3600)
            forecast[i]['time'] = forecast[i]['time'][0:3] + ' ' + forecast[i]['time'][11:16]
            forecast[i]['state'] = data['hourly'][hours_in_future]['weather'][0]['description']
            forecast[i]['temp'] = int(data['hourly'][hours_in_future]['temp'])
            forecast[i]['humidity'] = data['hourly'][hours_in_future]['humidity']  
            forecast[i]['icon'] = data['hourly'][hours_in_future]['weather'][0]['icon']
        
        i = i + 1
    

#create two copies of the same thing but one with html tags

#plain text !!!!

    text = f"Data for: {coords}"
    text = text + "------------------------------------------"


    for info in forecast:

        if info['time'] == time.ctime(time_of_req):
            text = text + f"Currently: {info['time']}"
        else:
            text = text + f" Forecast for: {info['time']}"

        text = text + f"- State: {info['state']} - Temperature: {info['temp']}C - R. Humidity: {info['humidity']}%"
        text = text + "------------------------------------------"
     
#end of plain text!!!!     
#html !!!

    html = '<font size="3">'

    html = html + f"Data for: {coords}<br>"
    html = html + "<hr><br>"
    
    for info in forecast:

        if info['time'] == time.ctime(time_of_req):
            html = html + f"<b>Currently: {info['time']}</b><br>"
        else:
            html = html + f"<b> Forecast for: {info['time']}</b><br>"

        html = html + f"&emsp;- State: {info['state']}<br>&emsp;- Temperature: {info['temp']}C<br>&emsp;- R. Humidity: {info['humidity']}%<br>"
        html = html + f"""<img src ="http://openweathermap.org/img/wn/{info['icon']}@2x.png"</img>"""
        html = html + "<br><hr><br>"

    html = html + "</font>"

#end of html !!!

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    return message

def send_email(sender_mail, receiver_email, message, time_sent):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    if log == True: 
        with open(log_path, 'a') as f:  
            f.write(f"Email sent to {receiver_email}, on {time_sent}\n")
        


    return


if __name__ == '__main__':
    main()