from django.shortcuts import render
import requests
from datetime import datetime, date
import random

quotes = [
    '<quote><h3>"There’s something about arriving in new cities, wandering empty streets with no destination. I will never lose the love for the arriving, but I\'m born to leave."</h3></quote> -Charlotte Eriksson, Empty Roads & Broken Bottles',
    '<quote><h3>"What strange phenomena we find in a great city, all we need do is stroll about with our eyes open. Life swarms with innocent monsters."</h3></quote> ― Charles Baudelaire',
    '<quote><h3>"Cities, like dreams, are made of desires and fears, even if the thread of their discourse is secret, their rules are absurd, their perspectives deceitful, and everything conceals something else."</h3></quote> ― Italo Calvino, Invisible Cities',
    '<quote><h3>"I love New York, even though it isn\'t mine, the way something has to be, a tree or a street or a house, something, anyway, that belongs to me because I belong to it."</h3></quote> ― Truman Capote',
    "<quote><h3>\"I don't know what London's coming to — the higher the buildings the lower the morals.\" ― Noël Coward, Collected Sketches and Lyrics",
    '<quote><h3>A city isn’t so unlike a person. They both have the marks to show they have many stories to tell. They see many faces. They tear things down and make new again."</h3></quote> ― Rasmenia Massoud, Broken Abroad',
]


def getrandomquote():
    URL = "http://127.0.0.1:8081/city_quotes/"
    quotes = requests.get(url=URL)
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
            "temp": temp,
            "sunrise": datetime.utcfromtimestamp(sunrise).strftime("%H:%M:%S"),
            "sunset": datetime.utcfromtimestamp(sunset).strftime("%H:%M:%S"),
            "quote": getrandomquote(),
        },
    )


# datetime.utcfromtimestamp(sunrise).strftime(%H:%M:%S)
# datetime.utcfromtimestamp(sunset).strftime(%H:%M:%S)
