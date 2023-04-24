from django.db import models

class Club(models.Model):
    nom = models.CharField(max_length=50)
    davlat = models.CharField(max_length=50)
    logo = models.FileField(blank=True, null=True)
    president = models.CharField(max_length=50)
    coach = models.CharField(max_length=50)
    yili = models.DateField()
    eng_qim_tr = models.CharField(max_length=100)
    eng_qim_sotuv = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Player(models.Model):
    ism = models.CharField(max_length=50)
    t_yil = models.DateField()
    tr_narxi = models.PositiveIntegerField()
    millat = models.CharField(max_length=50)
    pozitsiya = models.CharField(max_length=50, choices=(
        ('Forward', 'Forward'),
        ('Midfielder', 'Midfielder'),
        ('Defender', 'Defender'),
        ('Keeper', 'Keeper')
    ))
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ism} - {self.club}'

class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    eski = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='sotuvlari')
    yangi = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='sotib_olganlari')
    narxi = models.PositiveIntegerField()
    tax_narx = models.PositiveIntegerField()
    mavsum = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.player} - {self.mavsum}'

class Hozirgi_mavsum(models.Model):
    hozirgi_mavsum = models.CharField(max_length=100)

    def __str__(self):
        return self.hozirgi_mavsum