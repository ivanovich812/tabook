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
    # images = Image.objects.filter(melody_id=id)
    images = Image.objects.filter(melody_id=id).order_by("order_num")

    # for i in images:
    #     print(i.order_num)

    return render(request, 'show_melody.html', {'melody': melody, 'urls': urls, 'tabs': tabs, 'images': images})

def edit_melody(request, id):
    """Edit to melody"""
    try:
        melody = Melody.objects.get(id=id)
        urls = URL.objects.filter(melody_id=id)
        images = Image.objects.filter(melody_id=id).order_by("order_num")
        tabs = Tab.objects.filter(melody_id=id)

        if request.method == "POST":
            melody.name = request.POST.get("melody_name")
            melody.comment = request.POST.get("melody_comment")
            melody.save()

            # image.order_num = request.POST.get("order_num")
            # image.comment = request.POST.get("image_comment")
            # image.save()
            return HttpResponseRedirect(f"/edit_melody/{id}")
        else:
            return render(request, "edit_melody.html", {"melody": melody, "urls": urls, "tabs": tabs, "images": images})
    except Tab.DoesNotExist:
        return HttpResponseNotFound("<h2>Melody not found</h2>")

def add_url(request, id):
    if request.method == 'POST':
        form_url = URLForm(request.POST)

        if form_url.is_valid():
            new_url = form_url.save(commit=False)
            new_url.melody_id = id
            new_url = form_url.save()
            url_obj = form_url.instance
            return render(request, 'add_url.html', {'form_url': form_url, 'id': id})
    else:
        form_url = URLForm()
        return render(request, 'add_url.html', {'form_url': form_url, 'id':id})

def delete_url(request, melody_id, url_id):
    try:
        url = URL.objects.get(id=url_id)
        url.delete()
        return HttpResponseRedirect(f"/edit_melody/{melody_id}")
    except Tab.DoesNotExist:
        return HttpResponseNotFound("<h2>Melody not found</h2>")

def add_image(request, id):
    images = Image.objects.filter(melody_id=id).order_by("order_num")
    if images:
        lst = []
        for i in images:
            lst.append(i.order_num)
        max_order_num = max(lst)
    else:
        max_order_num = 0

    if request.method == 'POST':
        form_image = ImageForm(request.POST, request.FILES)

        if form_image.is_valid():
            new_img = form_image.save(commit=False)
            new_img.melody_id = id
            new_img = form_image.save()
            img_obj = form_image.instance
            return render(request, 'add_image.html', {'form_image': form_image, 'id': id})
    else:
        form_image = ImageForm(initial={'order_num': max_order_num+1})
        return render(request, 'add_image.html', {'form_image': form_image, 'id':id})

def delete_image(request, melody_id, image_id):
    try:
        Image.objects.get(id=image_id).path.delete(save=True)
        Image.objects.get(id=image_id).delete()

        # image = Image.objects.get(id=image_id).path.delete(save=True)
        # image.delete()

        return HttpResponseRedirect(f"/edit_melody/{melody_id}")
    except Tab.DoesNotExist:
        return HttpResponseNotFound("<h2>Image not found</h2>")

def edit_image(request, melody_id, image_id):
    image = Image.objects.get(id=image_id)
    path = image.path
    if request.method == 'POST':
        form_image = ImageForm(request.POST, request.FILES)

        if form_image.is_valid():
            img = form_image.save(commit=False)
            img.melody_id = melody_id
            img.id = image_id
            if str(img.path)=='':
                img.path = path
            img = form_image.save()
            img_obj = form_image.instance
            return render(request, 'edit_image.html', {'form_image': form_image, 'melody_id': melody_id, 'image_id': image_id})
    else:
        form_image = ImageForm(initial={'order_num': image.order_num, 'image_comment': image.image_comment})
        # form_melody = MelodyForm(initial={'date': datetime.datetime.now()})
        return render(request, 'edit_image.html', {'form_image': form_image, 'melody_id': melody_id, 'image_id': image_id})

def add_tab(request, id):
    pass
    if request.method == 'POST':
        form_tab = TabForm(request.POST)

        if form_tab.is_valid():
            new_tab = form_tab.save(commit=False)
            new_tab.melody_id = id
            new_tab = form_tab.save()
            tab_obj = form_tab.instance
            return render(request, 'add_tab.html', {'form_tab': form_tab, 'id': id})
    else:
        form_tab = TabForm()
        return render(request, 'add_tab.html', {'form_tab': form_tab, 'id':id})

def delete_tab(request, melody_id, tab_id):
    try:
        tab = Tab.objects.get(id=tab_id)
        tab.delete()
        return HttpResponseRedirect(f"/edit_melody/{melody_id}")
    except Tab.DoesNotExist:
        return HttpResponseNotFound("<h2>Tab not found</h2>")

def edit_tab(request, melody_id, tab_id):
    tab = Tab.objects.get(id=tab_id)
    if request.method == 'POST':
        form_tab = TabForm(request.POST)

        if form_tab.is_valid():
            tab = form_tab.save(commit=False)
            tab.melody_id = melody_id
            tab.id = tab_id
            img = form_tab.save()
            img_obj = form_tab.instance
            return render(request, 'edit_tab.html', {'form_tab': form_tab, 'melody_id': melody_id})
    else:
        form_tab = TabForm(initial={'tab': tab.tab})
        return render(request, 'edit_tab.html', {'form_tab': form_tab, 'melody_id': melody_id})