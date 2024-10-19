from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.db.models import Q
from django.db.models.functions import Lower
from django import forms
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from nimbus.models import Art, Comment, Like, Tag, Profile
from PIL import Image
import io

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'nimbus/custom_clearable_file_input.html'

class ImgProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_image',)
        widgets = {
            'profile_image': CustomClearableFileInput(attrs={'class': 'custom-file-input'})
        }

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

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'


    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_instance = self.instance

        if user_instance and user_instance.email == email:
            return email

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Este email já está em uso', code='invalid')
            )
        return email

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Digite seu comentário...'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ''
        self.fields['comment'].widget.attrs.update({'maxlength': '255',})

def index(request):
    posts = Art.objects.all().order_by('-created_date').prefetch_related(
        'likes', 'comments'
        )

    query = request.GET.get('search')
    selected_tag_id = request.GET.get('tag')

    if query:
        posts = posts.filter(Q(title__icontains=query))

    if selected_tag_id:
        posts = posts.filter(tags__id=selected_tag_id)

    paginator = Paginator(posts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all().order_by(Lower('name'))

    context = {
        'page_obj': page_obj,
        'title': 'Explorar',
        'tags': tags,
    }

    return render(
        request,
        'nimbus/index.html',
        context
    )


def post(request, post_id):
    single_post = get_object_or_404(Art, pk=post_id)
    site_title = f'{single_post.title}'

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.art = single_post
            comment.user = request.user
            comment.save()
            return redirect('nimbus:post', post_id=single_post.id)
    else:
        form = CommentForm()

    comments = single_post.comments.all()

    context = {
        'posts': single_post,
        'title': site_title,
        'form': form,
        'comments': comments,
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

            image_field = form.cleaned_data['image']
            image = Image.open(image_field)
            image_io = io.BytesIO()
            image.save(image_io, format='WEBP')

            webp_image = ContentFile(
                image_io.getvalue(), 
                name=f"{image_field.name.split('.')[0]}.webp"
            )
            
            post.image.save(webp_image.name, webp_image, save=False)
            post.save()
            form.save_m2m()

            messages.success(request, 'Publicado com sucesso!')
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
            return redirect('nimbus:login')
    else:
        form = RegisterForm()


    return render(
        request,
        'nimbus/create-user.html',
        {
            'form': form,
            'title': 'Cadastro',
        }
    )

def loginView(request):
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('nimbus:index')
        else:
            messages.error(request, 'Login inválido!')
            form.add_error(
                'password', ValidationError('Usuário ou senha inválidos!')
            )

    return render(
        request,
        'nimbus/login.html',
        {
            'form': form,
            'title': 'Login',
        }
    )

def logoutView(request):
    auth.logout(request)
    messages.success(request, 'Deslogado com sucesso!')
    return redirect('nimbus:index')


def like_art(request, art_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Você precisa estar logado para dar like.'}, status=403
            )

    art = get_object_or_404(Art, id=art_id)
    like, created = Like.objects.get_or_create(art=art, user=request.user)

    if not created:
        like.delete()

    return JsonResponse({'total_likes': art.likes.count()})

@login_required
def perfil(request, username):
    user = get_object_or_404(User, username=username)
    posts = Art.objects.filter(artist_id=user.id).prefetch_related(
        'likes', 'comments'
    )
    is_owner = request.user == user
    profile = user.profile

    form = RegisterForm(instance=user)
    del form.fields['username']
    img_form = ImgProfileForm(instance=profile)

    if request.user.username != username:
        return HttpResponseForbidden(
            "Você não tem permissão para acessar este perfil."
            )

    if request.method == 'POST':
        if 'edit-info' in request.POST:
            form = RegisterForm(request.POST, instance=user)
            del form.fields['username']
            if form.is_valid():
                form.save()
                messages.success(request, 'Editado com sucesso!')
                return redirect('nimbus:login')
            else:
                messages.error(request, 'Erro ao atualizar Informações pessoais')
                
        elif 'edit-image' in request.POST:
            img_form = ImgProfileForm(request.POST, request.FILES, instance=profile)
            if img_form.is_valid():
                img_form.save()
                messages.success(request, 'Imagem de perfil atualizada com sucesso!')
                return redirect('nimbus:perfil', username=user.username)
            else:
                messages.error(request, 'Erro ao atualizar foto de perfil')

        elif 'delete-posts' in request.POST:
            post_ids = request.POST.getlist('post_ids')
            if post_ids:
                Art.objects.filter(id__in=post_ids, artist_id=user.id).delete()
                messages.success(request, 'Posts deletados com sucesso!')
            else:
                messages.warning(request, 'Nenhum post foi selecionado.')

    context = {
        'form': form,
        'img_form': img_form,
        'posts': posts,
        'profile_user': user,
        'is_owner': is_owner,
        'title': f'{user.username}',
    }

    return render(
        request,
        'nimbus/user-perfil.html',
        context
    )

def sobre(request):

    context = {
        'title': 'Sobre',
    }

    return render(
        request,
        'nimbus/sobre.html',
        context
    )