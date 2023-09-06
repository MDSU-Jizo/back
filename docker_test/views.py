import json
import logging

from django.http import JsonResponse, HttpResponse
from .models import FakeEntity
from .forms import FakeEntityForm

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    try:
        form = FakeEntityForm({'title': 'test', 'text': 'Hello, world!'})

        if not form.is_valid():
            logger.error('Invalid form.')
            return JsonResponse({'code': 500, 'result': 'error', 'msg': 'Invalid form.'})

        form.save()
        data = FakeEntity.objects.latest('pk').get_title_text()
        logger.info('FakeEntity created.')
        return JsonResponse({'code': 200, 'result': 'success', 'msg': '', 'data': data})
    except:
        logger.exception('An Exception has occurred.')
        return JsonResponse({'code': 500, 'result': 'error', 'msg': 'An exception has occurred.'})