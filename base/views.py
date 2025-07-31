import base64
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render

def trigger_action(request):
    if request.method == "POST":
        action_type = request.POST.get("action")

        channel_layer = get_channel_layer()

        if action_type == "birthday":
            name = request.POST.get("name")
            photo = request.FILES.get("photo")

            # Convert image to base64
            image_data = photo.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            mime_type = photo.content_type
            image_url = f"data:{mime_type};base64,{image_base64}"

            async_to_sync(channel_layer.group_send)(
                "screen",
                {
                    "type": "send_action",
                    "action": action_type,
                    "data": {
                        "name": name,
                        "photo": image_url
                    }
                }
            )
            return render(request, "set.html")  # No need to pass context here

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
