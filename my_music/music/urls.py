from django.urls import path, include
from my_music.music import views

'''
◦ http://localhost:8000/ - home page
◦ http://localhost:8000/album/add/ - add album page
◦ http://localhost:8000/album/details/<id>/ - album details page
◦ http://localhost:8000/album/edit/<id>/ - edit album page
◦ http://localhost:8000/album/delete/<id>/ - delete album page
◦ http://localhost:8000/profile/details/ - profile details page
◦ http://localhost:8000/profile/delete/ - delete profile page
'''
urlpatterns = [
    path('', views.index, name='index'),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('album/', include([
        path('add/', views.add_album, name='add album'),
        path('details/<int:pk>/', views.details_album, name='details album'),
        path('edit/<int:pk>/', views.edit_album, name='edit album'),
        path('delete/<int:pk>/', views.delete_album, name='delete album'),
    ])),

    path('profile/', include([
        path('add_profile/', views.add_profile, name='add profile'),
        path('details/', views.details_profile, name='details profile'),
        path('delete/', views.delete_profile, name='delete profile'),
    ]))
]