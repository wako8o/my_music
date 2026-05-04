from django.contrib import admin

from my_music.music.models import Profile, Album


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass