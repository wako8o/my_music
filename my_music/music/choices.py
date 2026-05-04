from django.db.models import TextChoices


class GenreChoices(TextChoices):
    Metal = "Metal", 'Metal'
    Hard_Metal = "Hard Metal", 'Hard Metal'
    BG_Estrada_Music = "BG Estrada Music", 'BG Estrada Music'
    Chalga_Music = "Chalga Music", 'Chalga Music'
    Pop_Music ="Pop Music", 'Pop Music',
    Jazz_Music ="Jazz Music", 'Jazz Music',
    RB_Music = "R&B Music",  'R&B Music'
    Rock_Music = "Rock Music", 'Rock Music'
    Country_Music = "Country Music", 'Country Music'
    Dance_Music = "Dance Music", 'Dance Music'
    Hip_Hop_Music = "Hip Hop Music", 'Hip Hop Music'
    Other = "Other", 'Other'