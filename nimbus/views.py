from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ValidationError
from nimbus.models import Art

class PostForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = (
            'title', 'description', 'image', 'tags',
        )
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

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


@login_required
def createPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        context = {
            'form': form,
            'title': 'Criar',
            }

        if form.is_valid():
            post = form.save(commit=False)
            post.artist = request.user
            post.save()
            form.save_m2m()
            return redirect('nimbus:create')

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