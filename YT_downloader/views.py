from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from pytube import YouTube
# Create your views here.

def homepage(request):
    form = link_form()

    context = {'form' : form}
    return render(request,'index.html', context)



def result(request):

    if request.method == 'POST' :
        url = str(request.POST)
        print(url)

        video_obj = YouTube(url)

        video_streams = video_obj.streams.filter(file_extension='mp4')

        itag = []
        video_res = []

        for stream in video_streams:

            if stream.resolution and int(stream.resolution[:-1]) not in video_res:
                itag.append(stream.itag)
                video_res.append(int(stream.resolution[:-1]))
        
        video_res.sort(reverse=True)

        video_options = zip(itag,video_res)

        video_title = video_obj.title

        embed_link = video_obj.embed_url

        

    context = {'video_options':video_options, 'video_title':video_title, 'embed_link':embed_link,'url': url}

    return render(request,'result.html', context)


def download(request):

    if request.method == 'POST':
        print(request.POST)
        url = request.POST['link']
        choice = request.POST['choice']
        
        obj = YouTube(url).streams.get_by_itag(choice).download('~/Downloads')
    
    return redirect('home')
