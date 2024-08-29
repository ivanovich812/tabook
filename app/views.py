import datetime
import os

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .forms import MelodyForm, ImageForm, TabForm, URLForm
from .models import Melody, Image, Tab, URL


def index(request):
    melodies = Melody.objects.all()
    return render(request, "index.html", {"melodies": melodies})

def create_melody(request):
    if request.method == 'POST':
        form_melody = MelodyForm(request.POST)
        form_url = URLForm(request.POST)
        form_tab = TabForm(request.POST)
        form_img = ImageForm(request.POST, request.FILES)
        if form_melody.is_valid() and form_tab.is_valid() and form_url.is_valid() and form_img.is_valid():
            form_melody.save()
            melody_obj = form_melody.instance
            melody_id = melody_obj.id

            new_tab = form_tab.save(commit=False)
            new_tab.melody_id = melody_id
            new_tab = form_tab.save()
            tab_obj = form_tab.instance

            new_url = form_url.save(commit=False)
            new_url.melody_id = melody_id
            new_url = form_url.save()
            url_obj = form_url.instance

            new_img = form_img.save(commit=False)
            new_img.melody_id = melody_id
            new_img = form_img.save()
            img_obj = form_img.instance

            return render(request, 'create_melody.html', {
                'form_melody': form_melody,
                'form_tab': form_tab,
                'form_img': form_img,
                'form_url': form_url,
                'melody_obj': melody_obj,
                'tab_obj': tab_obj,
                'img_obj': img_obj,
                'url_obj': url_obj,
        })
    else:
        form_melody = MelodyForm(initial={'date': datetime.datetime.now()})
        form_tab = TabForm()
        form_img = ImageForm()
        form_url = URLForm()

    return render(request, 'create_melody.html', {
        'form_melody': form_melody,
        'form_tab': form_tab,
        'form_img': form_img,
        'form_url': form_url})

def delete_melody(request, id):
    try:
        melody = Melody.objects.get(id=id)
        melody.delete()
        return HttpResponseRedirect("/")
    except Tab.DoesNotExist:
        return HttpResponseNotFound("<h2>Melody not found</h2>")

def show_melody(request, id):
    """Show to melody uploaded by users"""
    melody = Melody.objects.filter(id=id)[0]
    urls = URL.objects.filter(melody_id=id)
    tabs = Tab.objects.filter(melody_id=id)
    images = Image.objects.filter(melody_id=id)
    return render(request, 'show_melody.html', {'melody': melody, 'urls': urls, 'tabs': tabs, 'images': images})

def edit_melody(request, id):
    """Edit to melody"""
    try:
        melody = Melody.objects.get(id=id)
        urls = URL.objects.filter(melody_id=id)

        if request.method == "POST":
            melody.name = request.POST.get("melody_name")
            melody.comment = request.POST.get("melody_comment")
            melody.save()
            return HttpResponseRedirect(f"/edit_melody/{id}")
        else:
            return render(request, "edit_melody.html", {"melody": melody, "urls": urls})
    except Tab.DoesNotExist:
        return HttpResponseNotFound("<h2>Melody not found</h2>")
