from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

IS_ACTIVE = (
        ('0', 'Tidak Aktif'),
        ('1', 'Aktif'),
        ('2', 'Hapus')
    )

class Pengguna(models.Model):
    no_hp = models.CharField(max_length=16, blank=False, default="Belum Diisi")
    id_login = models.ForeignKey(User, default="Nope")
    nama_user = models.CharField(max_length=32, blank=False, default="Belum Diisi")
    poto = models.ImageField(upload_to='user/potoprofile/%Y/%m', blank=True, null=False, default="media/noimage.png")
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.nama_user


class Kategori(models.Model):
    namakategori = models.CharField(max_length=32, blank=False, null=False)
    slug = models.CharField(max_length=32, blank=False, null=False)
    is_active = models.CharField(max_length=3, choices=IS_ACTIVE,default='1')
    created_by = models.CharField(max_length=32, blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.namakategori +" | " + self.is_active

    class Meta:
        ordering = ['namakategori']
    

class Material(models.Model):
    namamaterial = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField(unique=True)
    deskripsi = models.TextField(blank=True, default='tidak ada keterangan tentang produk ini')
    metafield = models.TextField(blank=True)
    gambar1 = models.ImageField(upload_to='gambar/material/%Y/%m', blank=True, null=False, default="media/noimage.png")
    gambar2 = models.ImageField(upload_to='gambar/material/%Y/%m', blank=True, null=False, default="media/noimage.png")
    gambar3 = models.ImageField(upload_to='gambar/material/%Y/%m', blank=True, null=False, default="media/noimage.png")
    gambar4 = models.ImageField(upload_to='gambar/material/%Y/%m', blank=True, null=False, default="media/noimage.png")
    gambar5 = models.ImageField(upload_to='gambar/material/%Y/%m', blank=True, null=False, default="media/noimage.png")
    is_active = models.CharField(max_length=3, choices=IS_ACTIVE,default='1')
    created_by = models.CharField(max_length=32, blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.namamaterial
  

class Product(models.Model):
    TAMPILHARGA = (
        ('0', 'Tidak Ditampilkan'),
        ('1', 'Tampilkan'),
    )   
    namaproduct = models.CharField(max_length=32, blank=False, null=False)
    deskripsi = models.TextField(blank=True, default='tidak ada keterangan tentang produk ini')
    material = models.ManyToManyField(Material)
    gambar1 = models.FileField(upload_to='gambar/product/%Y/%m', blank=True, null=False)
    gambar2 = models.FileField(upload_to='gambar/product/%Y/%m', blank=True, null=False)
    gambar3 = models.FileField(upload_to='gambar/product/%Y/%m', blank=True, null=False)
    gambar4 = models.FileField(upload_to='gambar/product/%Y/%m', blank=True, null=False)
    gambar5 = models.FileField(upload_to='gambar/product/%Y/%m', blank=True, null=False)
    kategori = models.ForeignKey('kategori', on_delete=models.CASCADE)
    is_active = models.CharField(max_length=3, choices=IS_ACTIVE,default='1')
    created_by = models.CharField(max_length=32, blank=False, null=True)
    harga = models.CharField(max_length=32, blank=False, default="0")
    show_harga = models.CharField(max_length=1, choices=TAMPILHARGA, default='2')
    slug = models.SlugField(unique=False, default='d')
    metafield = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.namaproduct



class Slider(models.Model):
    judul = models.CharField(max_length=32, blank=True)
    slug = models.CharField(max_length=64, blank=True)
    link = models.CharField(max_length=64, blank=True, null=True)    
    gambar = models.FileField(upload_to='gambar/slider/%Y/%m', blank=True, null=False)
    is_active = models.CharField(max_length=3, choices=IS_ACTIVE,default='1')    
    created_by = models.CharField(max_length=32)    
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.judul
