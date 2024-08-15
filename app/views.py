
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from classify import inference
from io import BytesIO
from PIL import Image
import numpy as np
import json
import base64
import json

from .redis import get_benefits


def homepage(request):
    second_page_url = reverse('details_page')
    ctx = {'details_page': second_page_url}
    return render(request, 'app/index.html', context=ctx)


def second_page(request):
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