"""kurniagranite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
    # Includ url from frontend
    url(r'^', include('frontend.urls')),
    # Office Admin
    url(r'^superoffice/', admin.site.urls),
    url(r'^office/$', views.index, name='officelogin'),
    url(r'^office/dashboard/$', views.homepage, name='homepage'),
    # Login
    url(r'^office/loginproses/$', views.loginproses, name='loginproses'),
    url(r'^office/logoutproses/$', views.logoutproses, name='logoutproses'),
    # Kategori
    url(r'^office/kategori/$', views.indexkategori, name="indexkategori"),
    url(r'^office/kategori/tambah/$', views.kategoritambah, name='kategoritambah'),
    url(r'^office/kategori/simpandata/$', views.kategorisimpan, name='kategorisimpan'),
    url(r'^office/kategori/aktifasi/(?P<slug>[\w-]+)/(?P<status>\d+)/$', views.kategoriaktifasi, name='kategoriaktifasi'),
    url(r'^office/kategori/hapus/(?P<slug>[\w-]+)/$', views.kategorihapus, name='kategorihapus'),    
    url(r'^office/kategori/ubah/(?P<slug>[\w-]+)/$', views.kategoriubah, name='kategoriubah'),    
    # Material
    url(r'^office/material/$', views.material, name='materialindex'),
    url(r'^office/material/tambah/$', views.materialtambah, name='materialtambah'),
    url(r'^office/material/simpandata/$', views.simpandata, name='materialprosestambah'),
    url(r'^office/material/detail/(?P<slug>[a-z])/$', views.detailmaterial, name='detailmaterial'),    
    url(r'^office/material/hapus/(?P<id>\d+)/$', views.hapusmaterial, name='materialhapus'),
    url(r'^office/material/aktifasi/(?P<slug>[\w-]+)/(?P<status>\d+)/$', views.aktifasimaterial, name='aktifasimaterial'),
    url(r'^office/material/ubah/(?P<id>\d+)/$', views.rubahdatamaterial, name='materialrubah'),
    # Produk
    url(r'^office/produk/$', views.indexproduk, name='indexproduk'),
    url(r'^office/produk/tambah/$', views.tambahproduk, name='produktambah'),
    url(r'^office/produk/simpandata/$', views.simpandataproduk, name='simpandataproduk'),
    url(r'^office/produk/aktifasi/(?P<slug>[\w-]+)/(?P<status>\d+)/$', views.aktifasiproduk, name='aktifasiproduk'),    
    url(r'^office/produk/hapus/(?P<slug>[\w-]+)/$', views.hapusproduk, name='produkhapus'),
    url(r'^office/produk/ubah/(?P<slug>[\w-]+)/$', views.ubahproduk, name='produkubah'),
    # Produk by kategori
    url(r'office/produk/(?P<kslug>[\w-]+)/$', views.productbykategori, name="productbykategori"),
    # Halaman Artikel
    url(r'office/slider/$', views.sliderindex, name='sliderindex'),
    url(r'office/slider/tambah/$', views.slidertambah, name='slidertambah'),
    url(r'office/slider/simpandata/$', views.simpandataslider, name='simpandataslider'),
    url(r'office/slider/aktifasi/(?P<slug>[\w-]+)/(?P<status>\d+)/$', views.aktifasiaslider, name='aktifasiaslider'),
    url(r'office/slider/ubah/(?P<slug>[\w-]+)/$', views.ubahslider, name='ubahdataslider'),
    url(r'office/slider/hapus/(?P<slug>[\w-]+)/$', views.hapuslider, name='hapuslider'),
    # Profile
    url(r'office/profile/$', views.profileindex, name='profileindex'),
    url(r'office/profile/ubah/$', views.profileubah, name='profileubah'),
    url(r'office/profile/profilesimpan/$', views.profilesimpan, name='profilesimpan')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


