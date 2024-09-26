from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth, messages
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

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, min_length=3,)
    last_name = forms.CharField(required=True, min_length=3,)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Este email já está em uso', code='invalid')
            )
        return email

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
            messages.success(request, 'Enviado com sucesso!')
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

def createUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso!')
            return redirect('nimbus:register')
    else:
        form = RegisterForm()


    return render(
        request,
        'nimbus/create-user.html',
        {
            'form': form
        }
    )