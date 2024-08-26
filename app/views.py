
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.urls import reverse
from classify import inference
from datetime import datetime
from io import BytesIO
from PIL import Image
import numpy as np
import json
import base64
import json
import uuid

from .tasks import delete_images, email_task
from .redis import get_benefits



def send_email(request):
    email_task.delay()
    return HttpResponse('Email sent!!!')


def homepage(request):
    second_page_url = reverse('details_page')
    second_page_url2 = reverse('details_page2')
    ctx = {'details_page': second_page_url,
           'details_page2': second_page_url2}
    return render(request, 'app/index.html', context=ctx)


def second_page(request):
    if request.method == "POST":
        if 'image' in request.FILES:
            image = request.FILES['image']
            filename = f'{datetime.now().strftime("%Y%m%d%H%M%S")}-{uuid.uuid4()}.{image.name.split(".")[-1]}'
            file_path = default_storage.save(filename, ContentFile(image.read()))
            # print(file_path)
            # file_url = default_storage.url(file_path)
        
            request.session['path'] = file_path
            return JsonResponse({'ok': True})
    
    image_path = request.session.get('path')
    if image_path:
            image_path = default_storage.path(image_path)
            # print(image_path)

            try:
                image = np.float32(Image.open(image_path))
            except FileNotFoundError:
                 return redirect('home')
            
            result = inference.fruit_classifier(image)
            fruit_name = result['fruit']
            ctx = get_benefits(fruit_name)
            delete_images.delay(image_path)
            return render(request, 'app/fruit_info.html', context=ctx)
    
    return render(request, 'app/fruit_info.html')  


# VIEW FOR CAMERA
# This view works if you are using JSON.stringify to send image
def second_page2(request):
    if request.method == "POST":
        data = json.loads(request.body)
        image_data = data.get('imageData')
        _, encoded = image_data.split(",", 1)
        request.session['image_data'] = encoded
        return JsonResponse({'ok': True})
    
    image_data = request.session.get('image_data')
    if image_data:
            image = base64.b64decode(image_data)
            image = np.float32(Image.open(BytesIO(image)))
            result = inference.fruit_classifier(image)
            fruit_name = result['fruit']
            ctx = get_benefits(fruit_name)
            return render(request, 'app/fruit_info.html', context=ctx)
    
    return render(request, 'app/fruit_info.html')  
