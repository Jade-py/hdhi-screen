import base64
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from datetime import date
from .models import Birthday
import time
import itertools

def trigger_action(request):
    if request.method == "POST":
        action_type = request.POST.get("action")

        channel_layer = get_channel_layer()

        if action_type == "birthday":
            curr_date = date.today()
            bday = Birthday.objects.filter(dob__month = curr_date.month, dob__day = curr_date.day)
            data = [
                {
                    "name": person.emp_name,
                    "photo": person.img.url if person.img else ""
                }
                for person in bday
            ]

            async_to_sync(channel_layer.group_send)(
                "screen",
                {
                    "type": "send_action",
                    "action": "birthday",
                    "data": data
                }
            )

            return render(request, "set.html")


        elif action_type == "play_daily_video":
            data = {"url": "/static/daily.mp4"}

        elif action_type == "play_bls_video":
            data = {"url": "/static/bls.mp4"}

        else:
            data = {"url": ""}

        async_to_sync(channel_layer.group_send)(
            "screen",
            {
                "type": "send_action",
                "action": action_type,
                "data": data
            }
        )

    return render(request, "set.html")

def show_screen(request):
    return render(request, 'index.html')
