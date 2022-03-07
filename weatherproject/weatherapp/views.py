from re import A
from django.shortcuts import render
import requests
from datetime import datetime, date
import random
from weatherproject.settings import API_KEY, API_URL


def getrandomquote():

    try:
        quotes = requests.get(
            url=API_URL, headers={"Authorization": "Api-Key " + API_KEY}
        )
    except:
        return "Our API Server is down so imagine there is a fancy quote here.. "

    quote_data = quotes.json()["data"]
    quote_texts = []
    for quote in quote_data:
        quote_texts.append(quote["attributes"]["quote"])
    return random.choice(quote_texts)


def index(request):
    if "city" in request.POST:
        city = request.POST["city"]
    else:
        city = "Berlin"

    appid = "645e55be388204571a9094e217998793"
    URL = "http://api.openweathermap.org/data/2.5/weather"
    PARAMS = {"q": city, "appid": appid, "units": "metric"}
    r = requests.get(url=URL, params=PARAMS)
    res = r.json()
    day = date.today()
    description = res["weather"][0]["description"]
    temp = res["main"]["temp"]
    sunrise = res["sys"]["sunrise"] + res["timezone"]
    sunset = res["sys"]["sunset"] + res["timezone"]

    return render(
        request,
        "weatherapp/index.html",
        {
            "city": city,
            "day": day,
            "description": description,
            "temp": round(temp),
            "sunrise": datetime.utcfromtimestamp(sunrise).strftime("%H:%M:%S"),
            "sunset": datetime.utcfromtimestamp(sunset).strftime("%H:%M:%S"),
            "quote": getrandomquote(),
        },
    )
