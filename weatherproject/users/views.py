import httpx
from asgiref.sync import sync_to_async

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings


async def index(request):
    context = {}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1:8001/users/users/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
        json = response.json()
        print(json)
        context["remote_users"] = json["data"]
    except httpx.RequestError as exc:
        context["connection_error"] = True

    return render(
        request,
        "users/index.html",
        context,
    )
