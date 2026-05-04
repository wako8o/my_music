from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_user_relations(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('music', 'Profile')
    Album = apps.get_model('music', 'Album')

    for profile in Profile.objects.filter(user__isnull=True):
        base_username = profile.username or f'profile_{profile.pk}'
        username = base_username
        idx = 1
        while User.objects.filter(username=username).exists():
            idx += 1
            username = f'{base_username}_{idx}'

        email = profile.email
        if not email:
            email = f'{username}@example.com'

        user = User.objects.create(username=username, email=email)
        profile.user = user
        profile.save(update_fields=['user'])

    fallback_user = User.objects.first()
    if fallback_user is None:
        fallback_user = User.objects.create(username='default_owner')

    for album in Album.objects.filter(owner__isnull=True):
        owner = Profile.objects.first().user if Profile.objects.exists() else fallback_user
        album.owner = owner
        album.save(update_fields=['owner'])


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_profile_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(assign_user_relations, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]

