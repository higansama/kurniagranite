from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from .serializers import *
from kurniagranite.tables import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
import re

MENU_KATEGORI_PRODUCT = Kategori.objects.all().filter(~Q(is_active=2))


def index(request):
    return render(request, 'kurniagranite/login.html')


# @login_required
def homepage(request):
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)    
    if not request.user.is_authenticated:
        return redirect('officelogin')
    return render(request, 'kurniagranite/homepage.html', {'title':'Homepage', 'menu_kategori_product':kategori, 'pengguna':FOTO_PENGGUNA})

def logoutproses(request):
    logout(request)
    return redirect('officelogin')

def loginproses(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active == True:
        login(request, user)
        kalimat = "Selamat Datang " + str(user.username)
        messages.success(request, kalimat)
        return redirect('homepage')
    else:
        return redirect('officelogin')
        




# profile
def profileindex(request):
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    if not request.user.is_authenticated:
        return redirect('officelogin')
    ob_user = User.objects.get(username=request.user)
    qs_pengguna = Pengguna.objects.filter(id_login=ob_user).count()
    if qs_pengguna == 0:
        qs_pengguna = Pengguna
    else:
        qs_pengguna = Pengguna.objects.get(id_login=ob_user)
    return render(request, 'kurniagranite/profile/index.html', {'menu_kategori_product':kategori, 'pengguna':qs_pengguna})

def profileubah(request):   
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    if not request.user.is_authenticated:
        return redirect('officelogin')
    ob_user = User.objects.get(username=request.user)
    qs_pengguna = Pengguna.objects.filter(id_login=ob_user).count()
    if qs_pengguna == 0:
        qs_pengguna = Pengguna
    else:
        qs_pengguna = Pengguna.objects.get(id_login=ob_user)
        # return HttpResponse(qs_pengguna)
    return render(request, 'kurniagranite/profile/form.html', {'menu_kategori_product':kategori, 'pengguna':qs_pengguna})

def profilesimpan(request):
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    if not request.user.is_authenticated:
        return redirect('officelogin')
    ob_user = User.objects.get(username=request.user)
    nama = request.POST.get('nama', 'Tidak Ada Data')
    nohp = request.POST.get('nomerhp', 'Tidak Ada Data')
    poto = request.FILES.get('poto')
    tipe = request.POST.get('tipe')
    id = request.POST.get('id')
    # return HttpResponse(tipe)
    if tipe == 'tambah':
        qs = Pengguna.objects.create(
            nama_user=nama,
            no_hp=nohp,
            poto=poto,
            id_login=ob_user
        )
        qs.save()
        return HttpResponse(qs)
    elif tipe == 'ubah':
        # return HttpResponse(id)
        qs = Pengguna.objects.get(id=id)
        qs.nama_user=nama
        qs.no_hp=nohp
        qs.poto=poto
        qs.id_login=ob_user
        qs.save()
        return redirect('profileindex')
        
        


# Kategori
def indexkategori(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    k = Kategori.objects.all().filter(~Q(is_active=2))
    qs_kategori = Kategori.objects.all().filter(~Q(is_active=2)).order_by('id')
    paginator = Paginator(qs_kategori, 30)
    page = request.GET.get('page',1)
    try:
        pkategori = paginator.page(page)
    except PageNotAnInteger:
        pkategori = paginator.page(page)
    except EmptyPage:
        pkategori = paginator.page(page)
    return render(request, 'kurniagranite/kategori/kategori.html', {'title':'Kategori', 'kategori':pkategori, 'menu_kategori_product':k, 'pengguna':FOTO_PENGGUNA})

def kategoritambah(request):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if not request.user.is_authenticated:
        return redirect('officelogin')
    kategori = Kategori.objects.all().filter(~Q(is_active=2)) 
    return render(request, 'kurniagranite/kategori/form.html', {'title':'Tambah data kategori', 'type':'tambah', 'menu_kategori_product':kategori, 'pengguna':FOTO_PENGGUNA})


def kategorisimpan(request):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if not request.user.is_authenticated:
        return redirect('officelogin')
    type = request.POST.get('type', 'lain')
    id = request.POST.get('id','')
    namakategori = request.POST.get('namakategori', 'Tidak Ada Data Yang Diterima')    
    slug = namakategori.replace(' ', '-').lower()
    if type == 'tambah':
        qs = Kategori.objects.create(namakategori=namakategori, slug=slug, created_by=str(request.user))
        qs.save()
        getid = Kategori.objects.get(slug=slug).id
        kalimat = "Data dengan nama <strong>" + str(namakategori) + "</strong> berhasil disimpan dengan nomer <strong>ID : " + str(getid) + "</strong>"
        messages.success(request, kalimat)
        return redirect('indexkategori')
    elif type == 'ubah':
        qs = Kategori.objects.get(pk=id)
        qs.namakategori = namakategori
        qs.slug = slug
        qs.save()
        getid = Kategori.objects.get(slug=slug).id        
        kalimat = "Data dengan nama <strong>" + str(namakategori) + "</strong> berhasil dirubah dengan nomer <strong>ID : " + str(getid) + "</strong>"
        messages.success(request, kalimat)
        return redirect('indexkategori')

def kategoriaktifasi(request, slug, status):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if not request.user.is_authenticated:
        return redirect('officelogin')
    qs = Kategori.objects.get(slug=slug)
    if status == '0':
        qs.is_active = 1
        qs.save()
        kalimat = "Nama Kategori : " + str(qs.namakategori) + "<br> Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('indexkategori')       
    else:
        qs.is_active = 0
        qs.save()
        kalimat = "Nama Kategori : " + str(qs.namakategori) + "<br>Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Non Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('indexkategori')

def kategoriubah(request, slug):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    qs = Kategori.objects.get(slug=slug)
    return render(request, 'kurniagranite/kategori/form.html' ,{'data':qs, 'title':"Rubah Data Kategori", 'kategori':kategori, 'type':'ubah', 'menu_kategori_product':MENU_KATEGORI_PRODUCT, 'pengguna':FOTO_PENGGUNA, 'lokasi':'kategori1'})

def kategorihapus(request, slug):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    qs = Kategori.objects.get(slug=slug)
    qs.delete()
    kalimat = "Data Berhasil Di Hapus"
    messages.success(request, kalimat)
    return redirect('indexkategori')





# ===========================Material
def material(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    datamaterial = Material.objects.all().filter(~Q(is_active=2))
    paginator = Paginator(datamaterial, 10)
    page = request.GET.get('page',1)
    # return HttpResponse(page)
    try:
        materials = paginator.page(page)
    except PageNotAnInteger:
        materials = paginator.page(page)
    except EmptyPage:
        materials = paginator.page(paginator.num_pages)
    return render(request, 'kurniagranite/material/material.html', {'title': 'Material', 'pmaterial':materials, 'menu_kategori_product':MENU_KATEGORI_PRODUCT, 'pengguna':FOTO_PENGGUNA, 'lokasi':'material', 
    'seluruhdata':datamaterial.count(),
    'dataaktif':datamaterial.filter(is_active=1).count(),
    'nonaktif':datamaterial.filter(is_active=0).count(),
     })

def materialtambah(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    return render(request, 'kurniagranite/material/rubah.html', {'title':'Tambah Data Material', 'type':'tambah', 'menu_kategori_product':kategori, 'pengguna':FOTO_PENGGUNA})


def simpandata(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)    
    id = request.POST.get('id', None)
    tipe = request.POST.get('type')
    namamaterial = request.POST.get('namamaterial')
    slug = namamaterial.replace(" ","-").lower()
    is_active = request.POST.get('status')
    deskripsi = request.POST.get('deskripsi')
    metafield = request.POST.get('tag')
    gambar1 = request.FILES.get('gambar1', "media/noimage.png")
    gambar2 = request.FILES.get('gambar2', "media/noimage.png")
    gambar3 = request.FILES.get('gambar3', "media/noimage.png")
    gambar4 = request.FILES.get('gambar4', "media/noimage.png")
    gambar5 = request.FILES.get('gambar5', "media/noimage.png")
    # for key, values in request.POST.lists():
    #     data = {key:values}
    # return HttpResponse(request.POST.lists())
            
    if tipe == 'tambah':
        if Material.objects.filter(namamaterial=namamaterial).count() >= 1:
            pesan = "nama sama"
            data = {"Status":"Failed"}
            messages.warning(request, 'Nama Material Harus Berbeda!')
            return render(request, 'kurniagranite/material/tambah.html', {'title':'Tambah Data Material', 'menu_kategori_product':MENU_KATEGORI_PRODUCT, 'type':'tambah', 'pengguna':FOTO_PENGGUNA})
        else:
            simpan = Material.objects.create(
                namamaterial=namamaterial,
                slug=slug,
                deskripsi=deskripsi,
                metafield=metafield,
                gambar1=gambar1,
                gambar2=gambar2,
                gambar3=gambar3,
                gambar4=gambar4,
                gambar5=gambar5,
                is_active=is_active,
                created_by=str(request.user),
            )
            pesan = "berhasil"
            data = Material.objects.get(namamaterial=namamaterial)
            status = {"Status":"Success"}
            kalimat = 'Data Sudah Disimpan Dengan Nomer ID :' + str(data.id)
            messages.success(request, kalimat)
            return redirect('materialindex') 
    elif tipe == 'ubah':
        qs = Material.objects.get(pk=id)
        qs.namamaterial = namamaterial
        qs.slug = slug
        qs.metafield = metafield
        if gambar1  == 'media/noimage.png':
            qs.gambar1  = qs.gambar1
        else:
            qs.gambar1 = gambar1
        
        if gambar2  == 'media/noimage.png':
            qs.gambar2  = qs.gambar2
        else:
            qs.gambar2 = gambar2

        if gambar3  == 'media/noimage.png':
            qs.gambar3  = qs.gambar3
        else:
            qs.gambar3 = gambar3

        if gambar4  == 'media/noimage.png':
            qs.gambar4  = qs.gambar4
        else:
            qs.gambar4 = gambar4

        if gambar5  == 'media/noimage.png':
            qs.gambar5  = qs.gambar5
        else:
            qs.gambar5 = gambar5
        qs.is_active = is_active
        created_by = str(request.user)
        qs.save()
        data = Material.objects.get(namamaterial=namamaterial)
        kalimat = "Data Dengan ID "+ str(data.id)+" Sudah Berhasil Di Rubah"
        messages.success(request, kalimat)
        return redirect('materialindex') 
        


def detailmaterial(request, slug):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)    
    data = Material.objects.get(slug=slug)
    return render(request, 'kurniagranite/material/detail.html', {'title':'Detail Material' + data.namamaterial, 'data' : data, 'menu_kategori_product':MENU_KATEGORI_PRODUCT, 'pengguna':FOTO_PENGGUNA})


def aktifasimaterial(request, slug, status):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    qs = Material.objects.get(slug=slug)
    if status == '0':
        qs.is_active = 1
        qs.save()
        kalimat = "Nama Material : " + str(qs.namamaterial) + "<br> Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('materialindex')       
    else:
        qs.is_active = 0
        qs.save()
        kalimat = "Nama Material : " + str(qs.namamaterial) + "<br>Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Non Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('materialindex')

def hapusmaterial(request, id):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if Material.objects.get(pk=id).is_active != "2":
        qs = Material.objects.get(pk=id)
        qs.is_active = "2"
        qs.save()
        kalimat = 'Data Sudah Di<strong>Hapus</strong>'
        messages.success(request, kalimat)
        return redirect('materialindex')
    else:
        return redirect('materialindex')

def rubahdatamaterial(request, id):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    qs = Material.objects.get(pk=id)
    return render(request, 'kurniagranite/material/rubah.html', {'title':'Ubah Data', 'data':qs, 'type':'ubah', 'n':range(1,6,1), 'menu_kategori_product':MENU_KATEGORI_PRODUCT, 'pengguna':FOTO_PENGGUNA, 'lokasi':'kategori1'})




# Produk
def indexproduk(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    dataproduct = Product.objects.all().filter(~Q(is_active=2))
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    paginator = Paginator(dataproduct, 10)
    page = request.GET.get('page',1)
    try:
        pproducts = paginator.page(page)
    except PageNotAnInteger:
        pproducts = paginator.page(page)
    except EmptyPage:
        pproducts = paginator.page(paginator.num_pages)
    return render(request, 'kurniagranite/produk/produk.html', {'title': 'produk', 'pproduct':pproducts, 'menu_kategori_product':kategori, 'pengguna':FOTO_PENGGUNA,
    'seluruhdata':dataproduct.count(),
    'dataaktif':dataproduct.filter(is_active=1).count(),
    'nonaktif':dataproduct.filter(is_active=0).count(),
    })

def tambahproduk(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    qs_material = Material.objects.all().filter(~Q(is_active=2))    
    return render(request, 'kurniagranite/produk/form.html', {'title':'Tambah Produk','type':'tambah', 'kategori':kategori, 'material':qs_material, 'menu_kategori_product':kategori, 'pengguna':FOTO_PENGGUNA})

def ubahproduk(request, slug):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2)) 
    qs = Product.objects.get(slug=slug)
    qs_material = Material.objects.all().filter(~Q(is_active=2))        
    used_material = qs.material.all()
    return render(request, 'kurniagranite/produk/form.html', {'title':'Ubah Data Produk', 'type':'ubah', 'id': qs.id, 'data':qs, 'usedmaterial': used_material, 'material':qs_material, 'kategori':kategori , 'pengguna':FOTO_PENGGUNA})


def simpandataproduk(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    tipe = request.POST.get('type', 'tambah')
    k_id = request.POST.get('kategori','Tidak ada data')
    kategori = Kategori.objects.get(id=k_id)
    namaproduk = request.POST.get('namaproduk', 'Tida Ada Data')
    status = request.POST.get('status', '0')
    tag = request.POST.get('tag', 'Tidak ada data')
    slug = namaproduk.lower().replace(" ","-")
    deskripsi = request.POST.get('deskripsi', 'Belum ada deskripsi')
    gambar1 = request.FILES.get('gambar1', 'media/noimage.png')
    gambar2 = request.FILES.get('gambar2', "media/noimage.png")
    gambar3 = request.FILES.get('gambar3', "media/noimage.png")
    gambar4 = request.FILES.get('gambar4', "media/noimage.png")
    gambar5 = request.FILES.get('gambar5', "media/noimage.png")
    usedmaterial = request.POST.getlist('usedmaterial')
    hargaproduk = request.POST.get('hargaproduk')
    show_harga = request.POST.get('showprice')
    if tipe == 'tambah':
        if not request.user.is_authenticated:
            return redirect('officelogin')
        if Product.objects.filter(namaproduct=namaproduk).count() >= 1:
            kalimat = "Nama Product : " + namaproduk + "<br> Sudah ada, harap gunakan nama lain untuk menghindari kesalahan"
            messages.success(request, kalimat)
            return redirect('produktambah')
        else:
            qs = Product.objects.create(
            namaproduct = namaproduk,
            slug=slug,
            kategori = kategori,
            deskripsi = deskripsi,
            harga = hargaproduk,
            show_harga = show_harga,
            metafield = tag,
            created_by=str(request.user),
            gambar1  = gambar1,
            gambar2  = gambar2,
            gambar3  = gambar3,
            gambar4  = gambar4,
            gambar5  = gambar5,
            )
            qs.save()
            for i in usedmaterial:
                m = Material.objects.get(slug=i)
                qs.material.add(m)
                qs.save()
            qs.save()
            kalimat = "Nama Product : " + namaproduk + "<br> <strong>Berhasil Disimpan</strong>, dengan ID: "+str(qs.namaproduct)
            messages.success(request, kalimat)
            return redirect('indexproduk')
    elif type == 'ubah':
        if not request.user.is_authenticated:
            return redirect('officelogin')
        qs = Product.objects.get(namaproduct=namaproduk)
        qs.namaproduct = namaproduk
        qs.slug=slug
        qs.kategori = kategori
        qs.deskripsi = deskripsi
        qs.harga = hargaproduk
        qs.show_harga = show_harga
        qs.metafield = tag
        if gambar1  == 'media/noimage.png':
            qs.gambar1  = qs.gambar1
        else:
            qs.gambar1 = gambar1

        if gambar2  == 'media/noimage.png':
            qs.gambar2  = qs.gambar2
        else:
            qs.gambar2 = gambar2

        if gambar3  == 'media/noimage.png':
            qs.gambar3  = qs.gambar3
        else:
            qs.gambar3 = gambar3

        if gambar4  == 'media/noimage.png':
            qs.gambar4  = qs.gambar4
        else:
            qs.gambar4 = gambar4

        if gambar5  == 'media/noimage.png':
            qs.gambar5  = qs.gambar5
        else:
            qs.gambar5 = gambar5
        qs.save()
        for i in usedmaterial:
            m = Material.objects.get(slug=i)
            qs.material.add(m)
            qs.save()
        qs.save()
        kalimat = "Nama Product : " + namaproduk + "<br> <strong>Berhasil Disimpan</strong>, dengan ID: "+str(Product.objects.get(namaproduct=namaproduk).id)
        messages.success(request, kalimat)
        return redirect('indexproduk')        
    return redirect('indexproduk')



def aktifasiproduk(request, slug, status):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    qs = Product.objects.get(slug=slug)
    if status == '0':
        if not request.user.is_authenticated:
            return redirect('officelogin')
        qs.is_active = 1
        qs.save()
        kalimat = "Nama Produk : " + str(qs.namaproduct) + "<br> Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('indexproduk')       
    else:
        if not request.user.is_authenticated:
            return redirect('officelogin')
        qs.is_active = 0
        qs.save()
        kalimat = "Nama Produk : " + str(qs.namaproduct) + "<br>Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Non Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('indexproduk')



def hapusproduk(request, slug):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    qs = Product.objects.get(slug=slug)
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if qs.is_active != 2:
        if not request.user.is_authenticated:
            return redirect('officelogin')
        hapus = qs.delete()
        kalimat = "Nama Produk : " + str(qs.namaproduct) + "<br>Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Di Hapus</strong> "
        messages.success(request, kalimat)
        return redirect('indexproduk')
    else:
        if not request.user.is_authenticated:
            return redirect('officelogin')
        kalimat = "Data Gagal Di hapus"
        messages.success(request, kalimat)
        return redirect('indexproduk')
    




# Product By Categori
def productbykategori(request, kslug):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)    
    if not request.user.is_authenticated:
        return redirect('officelogin')
    get_kategori = Kategori.objects.get(slug=kslug)   
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    qs_product = Product.objects.filter(kategori=get_kategori)
    # dataproduct = Product.objects.all().filter(~Q(is_active=2))
    kategori = Kategori.objects.all().filter(~Q(is_active=2))    
    paginator = Paginator(qs_product, 10)
    page = request.GET.get('page',1)
    try:
        pproducts = paginator.page(page)
    except PageNotAnInteger:
        pproducts = paginator.page(page)
    except EmptyPage:
        pproducts = paginator.page(paginator.num_pages)
    return render(request, 'kurniagranite/produk/produkbykategori.html', {'title': 'produk', 'pmaterial':pproducts, 'kategori':kategori, 'menu_kategori_product':MENU_KATEGORI_PRODUCT, 'pengguna':FOTO_PENGGUNA, 'lokasi':'kategori',
    'seluruhdata':qs_product.count(),
    'dataaktif':qs_product.filter(is_active=1).count(),
    'nonaktif':qs_product.filter(is_active=0).count(),
    })



# Slider
def sliderindex(request):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    qs_slider = Slider.objects.all().filter(~Q(is_active=2))
    paginator = Paginator(qs_slider, 10)
    page = request.GET.get('page',1)
    try:
        slider = paginator.page(page)
    except PageNotAnInteger:
        slider = paginator.page(page)
    except EmptyPage:
        slider = paginator.page(page)
    # return HttpResponse(slider)
    return render(request, 'kurniagranite/slider/slider.html', {'title':'Slider Index', 'menu_kategori_product':kategori, 'slider':slider, 'pengguna':FOTO_PENGGUNA})        

def slidertambah(request):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if not request.user.is_authenticated:
        return redirect('officelogin')
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    return render(request, 'kurniagranite/slider/form.html', {'title':'Tambah Data Slider', 'type':'tambah', 'menu_kategori_product':kategori, 'pengguna':FOTO_PENGGUNA, 'lokasi':'kategori'})

def ubahslider(request, slug):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    if not request.user.is_authenticated:
        return redirect('officelogin')
    qs_slider = Slider.objects.get(slug=slug)
    return render(request, 'kurniagranite/slider/form.html', {'title':'Ubah Data Slider', 'type':'ubah', 'menu_kategori_product':kategori, 'data':qs_slider, 'pengguna':FOTO_PENGGUNA, 'lokasi':'slider'})
        

def aktifasiaslider(request, slug, status):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if not request.user.is_authenticated:
        return redirect('officelogin')
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    qs = Slider.objects.get(slug=slug)
    if status == '0':
        qs.is_active = 1
        qs.save()
        kalimat = "Slider : " + str(qs.judul) + "<br> Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('sliderindex')       
    else:
        qs.is_active = 0
        qs.save()
        kalimat = "Nama Produk : " + str(qs.judul) + "<br>Data dengan ID: " + str(qs.pk) + " berhasil di <strong>Non Aktifkan</strong> "
        messages.success(request, kalimat)
        return redirect('sliderindex')


def simpandataslider(request):
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    if not request.user.is_authenticated:
        return redirect('officelogin')
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    id = request.POST.get('id', False)
    tipe = request.POST.get('type', False)
    judul = request.POST.get('judul', False)
    slug = judul.lower().replace(" ","-")
    link = request.POST.get('link', "Tidak Menyertakan Link")
    status = request.POST.get('status', '1')
    gambar = request.FILES.get('gambar', 'media/noimage.png')
    if tipe == "tambah":
        cek = Slider.objects.filter(judul=judul).count()
        if cek >= 1:
            kalimat = "Data Gagal Di Buat Karena Ada Judul Yang Sama"
            messages.success(request, kalimat)
            return redirect('sliderindex')
        else:
            qs = Slider.objects.create(
            judul = judul,
            is_active = status,
            link = link,
            slug = slug,
            created_by = str(request.user),
            gambar = gambar)
            qs.save()
            cek = Slider.objects.get(judul=judul).id
            kalimat = "Data Berhasil Di Buat Dengan Id " + str(cek)
            messages.success(request, kalimat)
            return redirect('sliderindex')
    elif tipe == "ubah":
        if not request.user.is_authenticated:
            return redirect('officelogin')
        qs = Slider.objects.get(pk=id)
        qs.judul = judul
        qs.is_active = status
        qs.link = link
        qs.slug = slug        
        qs.save()
        if gambar  == 'media/noimage.png':
            qs.gambar  = qs.gambar
        else:
            qs.gambar = gambar
        qs.save()
        cek = Slider.objects.get(judul=judul).id
        kalimat = "Data Berhasil Di Ubah Dengan Id " + str(cek)
        messages.success(request, kalimat)
        return redirect('sliderindex')
    else:
        messages.success(request, "Gagal")        
        return redirect('sliderindex')

def hapuslider(request, slug):
    if not request.user.is_authenticated:
        return redirect('officelogin')
    FOTO_PENGGUNA = Pengguna.objects.get(id_login=request.user)
    kategori = Kategori.objects.all().filter(~Q(is_active=2))
    qs = Slider.objects.get(slug=slug)
    qs.delete()
    kalimat = "Data dengan id : <strong>" + str(qs.id) + "</strong> berhasil di hapus."
    messages.success(request, "Gagal")        
    return redirect('sliderindex')