import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings


@csrf_exempt
def upload_file(request):
    upload = request.FILES.get('upload')
    uid = ''.join(str(uuid.uuid4()).split('-'))
    names = str(upload.name).split('.')
    names[0] = uid
    upload.name = '.'.join(names)
    new_path = os.path.join(settings.MEDIA_ROOT, 'upload/', upload.name)
    with open(new_path, 'wb+') as file:
        for chunk in upload.chunks():
            file.write(chunk)

    filename = upload.name
    url = '/media/upload/' + filename
    retdata = {'url': url,
               'uploaded': '1',
               'fileName': filename}
    return JsonResponse(retdata)