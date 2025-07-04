from django.shortcuts import render, redirect
from .models import File
from .forms import FileForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def set_photo_or_video(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            File.objects.all().delete()
            file_instance = form.save()

            # Notify via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "screen",
                {
                    "type": "send_file",
                    "file_url": file_instance.file.url
                }
            )

            return redirect('set')
    else:
        form = FileForm()
    return render(request, 'set.html', {'form': form})

def show_screen(request):
    file = File.objects.first()
    return render(request, 'index.html', {'file':file})
