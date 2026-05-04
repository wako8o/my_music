from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from my_music.music.models import Profile, Album


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'email']

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                }),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Email',
                }),
            'age': forms.TextInput(
                attrs={
                    'placeholder': 'Age',
                }),
        }

class ProfileCreateForm(ProfileBaseForm):
    pass

class ProfileDeleteForm(ProfileBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_hidden_fields()

        if 'photo' in self.fields:
            self.fields.pop('photo')

        self._make_fields_not_required()

    def save(self, commit=True):
        if commit:
            if self.instance.user_id:
                Album.objects.filter(owner=self.instance.user).delete()

            try:
                if getattr(self.instance, 'photo', None):
                    self.instance.photo.delete(save=False)
            except Exception:
                pass

            if self.instance.user_id:
                self.instance.user.delete()
            else:
                self.instance.delete()

        return self.instance

    def _set_hidden_fields(self):
        for _, field in self.fields.items():
            field.widget = forms.HiddenInput()

    def _make_fields_not_required(self):
        for _, field in self.fields.items():
            field.required = False




class AlbumBaseForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['owner']
        widgets = {
            'album_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de album',
                }
            ),

            'artist': forms.TextInput(
                attrs={
                    'placeholder': 'Artist',
                }
            ),

            'descriptions': forms.Textarea(
                attrs={
                    'placeholder': 'Descripciones',
                }
            ),

            'image_url': forms.TextInput(
                attrs={
                    'placeholder': 'Imagen URL',
                }
            ),

            'price': forms.TextInput(
                attrs={
                    'placeholder': '0.0',
                }
            )
        }

class AlbumCreateForm(AlbumBaseForm):
    pass

class AlbumEditForm(AlbumBaseForm):
    pass

class AlbumDeleteForm(AlbumBaseForm):
    def save(self, commit=True):
        if commit:
            self.instance.delete()

        return self.instance


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))


