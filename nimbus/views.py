from typing import Any
from django.shortcuts import render, get_object_or_404
from django import forms
from django.core.exceptions import ValidationError
from nimbus.models import Art

class PostForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = (
            'title', 'description', 'image', 'tags',
        )
    
    def clean(self):
        cleaned_data = self.cleaned_data

        self.add_error(
            'title',
            ValidationError(
                'Mensagem de erro',
                code='invalid'
            )
        )
        return super().clean()



def index(request):
    posts = Art.objects.all().prefetch_related('likes', 'comments') 

    context = {
        'posts': posts,
        'title': 'Explorar',
    }

    return render(
        request,
        'nimbus/index.html',
        context
    )



def post(request, post_id):
    single_post = get_object_or_404(Art.objects, pk=post_id)
    site_tile = f'{single_post.title}'

    context = {
        'posts': single_post,
        'title': site_tile,
    }

    return render(
        request,
        'nimbus/post.html',
        context
    )



def createPost(request):
    if request.method == 'POST':
        context = {
            'form': PostForm(request.POST),
            'title': 'Criar',
            }

        return render(
            request,
            'nimbus/create-post.html',
            context
        )

    context = {
        'form': PostForm(),
        'title': 'Criar',
    }

    return render(
        request,
        'nimbus/create-post.html',
        context
    )