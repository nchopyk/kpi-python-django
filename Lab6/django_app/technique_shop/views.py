from django.http import HttpResponse
from .models import Technique
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def get_technique_list(request):
    all_technique = Technique.objects.all()

    template = loader.get_template('technique_list.html')
    context = {
        'techniques': all_technique,
    }

    return HttpResponse(template.render(context, request))


def get_technique_by_id(request, technique_id):
    technique = Technique.objects.get(pk=technique_id)

    template = loader.get_template('technique_detail.html')
    context = {
        'technique': technique,
    }

    return HttpResponse(template.render(context, request))


def get_about_info(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({}, request))
