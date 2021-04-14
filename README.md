# Weather-Bot
Python app that sends e-mails with weather forecasts. It's designed to run daily on Linux systems using cronjob

# Disclaimer
This software is not meant for beginners, as basic code literacy and some tech skills are required.
I've used raspberryPi 4B with raspbian to run this software.

# How to use it

1. Gather the list of recipients alongside with the corresponding coordinates of the desired location (for what place to get weather data) and how many hours in the future should the forecasts be for (explained in the "Data" section below).
2. Supply the data in the correct format (explained in the "Data" section below) to the "reciever_list.json" file.
3. Register an account on the e-mail/SMTP host of your choice (e.g. gmail or outlook)
4. Register an Open Weather API account and get the API key.
5. Open the weather_bot.py file and modify the variables in the Config section, based on your credentials and needs.
6. Setup a Linux enviroment with python3 installed
7. Firstly use the "chmod 701 /PATH/weather_bot.py" to make the script executable (you can change the number), then edit the crontab with "crontab -e" and set the time at which the script is to be run (once per day at a set time is recommended).
8. Everything should be up and running now.


# Data
The reciever_list.json file contains a list of all recipients. Each recipient consists of a dictionary:
1. "address": "email address"
2. "coords": two element list with coordinates [latitude, longtitude]
3. "forecasts": n-element list in which every number corresponds to how much in the future the forecasts should be. For example [0, 10, 20] will produce 3 data sets. 0 is for current weather, 10 will return a forecast for T+10 hours, 20 will return a forecast for T+20 hours. Each additional number put in here will result in an email containing additional section.

I provided an example of how should the reciever_list.json file look like.

