from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from my_music.music.forms import (
    ProfileCreateForm,
    AlbumCreateForm,
    AlbumEditForm,
    AlbumDeleteForm,
    ProfileDeleteForm,
    SignUpForm,
    SignInForm,
)
from my_music.music.models import Profile, Album


def get_profile(user):
    if not user.is_authenticated:
        return None
    return Profile.objects.filter(user=user).first()


def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('add profile')
    else:
        form = SignUpForm()

    return render(request, 'auth/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = SignInForm(request)

    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = get_profile(request.user)
    if profile is None:
        return redirect('add profile')

    albums = Album.objects.filter(owner=request.user)
    context = {
        'profile': profile,
        'albums': albums,
    }

    return render(request, 'core/home-with-profile.html', context)


@login_required
def add_album(request):
    if get_profile(request.user) is None:
        return redirect('add profile')

    if request.method == 'GET':
        form = AlbumCreateForm()
    else:
        form = AlbumCreateForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            return redirect('index')

    # form = AlbumCreateForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     album = form.save(commit=False)
    #     album.user = request.user
    #     album.save()
    #     return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'album/add-album.html', context)


@login_required
def details_album(request, pk):
    album = get_object_or_404(Album, pk=pk, owner=request.user)

    context = {
        'album': album,
    }

    return render(request, 'album/album-details.html', context)


@login_required
def edit_album(request, pk):
    album = get_object_or_404(Album, pk=pk, owner=request.user)
    if request.method == 'GET':
        form = AlbumEditForm(instance=album)
    else:
        form = AlbumEditForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form,
        'album': album,
    }
    return render(request, 'album/edit-album.html', context)


@login_required
def delete_album(request, pk):
    album_delete = get_object_or_404(Album, pk=pk, owner=request.user)
    if request.method == 'GET':
        form = AlbumDeleteForm(instance=album_delete)
        
    else:
        form = AlbumDeleteForm(request.POST, instance=album_delete)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form,
        'album_delete': album_delete,
    }
    return render(request, 'album/delete-album.html', context)


@login_required
def add_profile(request):
    if get_profile(request.user):
        return redirect('index')

    if request.method == 'GET':
        form = ProfileCreateForm()
    else:
        form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('index')

    context = {
        'form': form,
        'add_album': True,
    }
    return render(request, 'core/home-no-profile.html', context)



@login_required
def details_profile(request):
    profile = get_profile(request.user)
    if profile is None:
        return redirect('add profile')
    albums = Album.objects.filter(owner=request.user).count()

    context = {
        'profile': profile,
        'albums': albums,
    }

    return render(request, 'profile/profile-details.html', context)


@login_required
def delete_profile(request):
    profile = get_profile(request.user)
    if profile is None:
        return redirect('add profile')

    if request.method == 'GET':
        form = ProfileDeleteForm(instance=profile)
    else:
        form = ProfileDeleteForm(request.POST, instance=profile)
        if form.is_valid():
            logout(request)
            form.save()
            return redirect('login')

    context = {
        'form': form,
        }

    return render(request, 'profile/profile-delete.html', context)