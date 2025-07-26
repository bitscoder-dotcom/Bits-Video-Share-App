from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')
def video_list(request):
    return render (request, 'video')