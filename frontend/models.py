from django.db import models
from django.contrib.auth.models import User

# Create your models here.
IS_ACTIVE = (
        ('0', 'Tidak Aktif'),
        ('1', 'Aktif'),
        ('2', 'Hapus')
    )
class Pelanggan(models.Model):
    #pastikan is staff selalu false ketika input data ke pelanggan
    username  = models.CharField(max_length=32, blank=False, null=False)
    email  = models.CharField(max_length=32, blank=False, null=False)
    alamat = models.TextField()
    tipe  = models.CharField(max_length=2, blank=False, null=False)
    id_login = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.CharField(max_length=3, choices=IS_ACTIVE,default='1')
    created_by = models.CharField(max_length=32, blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.username

