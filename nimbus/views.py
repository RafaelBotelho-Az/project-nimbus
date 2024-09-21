from django.shortcuts import render
from nimbus.models import Art



def index(request):
    posts = Art.objects.all()

    context = {
        'posts': posts,
    }

    return render(
        request,
        'nimbus/index.html',
        context
    )