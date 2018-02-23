from django.shortcuts import render, get_object_or_404, redirect
from kurniagranite.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

KATEGORI = Kategori.objects.all().filter(~Q(is_active=2))
SLIDER = Slider.objects.all().filter(~Q(is_active=2))

def beranda(request):
    KATEGORI = Kategori.objects.all().filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    PRODUCT = Product.objects.all().filter(~Q(is_active=2)).order_by('?')[:8]
    MATERIAL = Material.objects.all().filter(~Q(is_active=2)).order_by('?')[:8]
    return render(request, 'frontend/index.html', {'title':'Beranda', 'kategori':KATEGORI, 'produk':PRODUCT, 'material':MATERIAL })

def fproductbykategori(request, slug):
    KATEGORI = Kategori.objects.all().filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    qs_kategori = Kategori.objects.filter(slug=slug)
    qs_product = Product.objects.filter(kategori=qs_kategori)
    susun = request.GET.get('sorting')
    if susun is False:
        qs_product = Product.objects.filter(~Q(is_active=2)).filter(kategori=qs_kategori).order_by('kategori')
    elif susun == 'newest':
        qs_product = Product.objects.filter(~Q(is_active=2)).filter(kategori=qs_kategori).order_by('date_created')
    elif susun == 'oldest':
        qs_product = Product.objects.filter(~Q(is_active=2)).filter(kategori=qs_kategori).order_by('-date_created')
    elif susun  == 'atoz':
        qs_product = Product.objects.filter(~Q(is_active=2)).filter(kategori=qs_kategori).order_by('namaproduct')
    elif susun == 'ztoa':
        qs_product = Product.objects.filter(~Q(is_active=2)).filter(kategori=qs_kategori).order_by('-namaproduct')
    else:
        qs_product = Product.objects.filter(~Q(is_active=2)).filter(kategori=qs_kategori).order_by('kategori')
    if qs_kategori.count() == 0:
        return redirect("frontend:notfoundpage")
    else:
        paginator = Paginator(qs_product, 12)
        page = request.GET.get('page',1)
        try:
            produk = paginator.page(page)
        except PageNotAnInteger:
            produk = paginator.page(page)
        except EmptyPage:
            produk = paginator.page(page)
        return render(request, 'frontend/productbykategori.html', {'produk':produk,
                                                    'lokasi':'bk',
                                                    'title': 'Produk Dari Kategori ' + str(Kategori.objects.get(slug=slug).namakategori),
                                                    'kategori':KATEGORI,
                                                    'produk':produk,
                                                    'slug': slug,
                                                    })


# Material
def allmaterial(request):
    KATEGORI = Kategori.objects.all().filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    qs_material = Material.objects.all().filter(~Q(is_active=2))
    return render(request, 'frontend/material.html', {'title':'Material', 'kategori':KATEGORI,'material':qs_material, 'slider':SLIDER})

def detailmaterial(request, slug):
    KATEGORI = Kategori.objects.all().filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    qs_material = Material.objects.filter(slug=slug)
    if qs_material.count() == 0:
        return redirect("frontend:notfoundpage")
    else:
        m = Material.objects.get(slug=slug)
        qs_produk = Product.objects.filter(material__id=m.id).order_by('?')[:4]
        if qs_produk.count() == 0:
            qs_produk = Product.objects.all().order_by('?')[:4]
        return render(request, 'frontend/detailmaterial.html', {'title':'Detail Material',
                                                                'kategori':KATEGORI,
                                                                'material':m,
                                                                'produk':qs_produk,
                                                                'slider':SLIDER})

# artwork
def artwork(request):
    KATEGORI = Kategori.objects.filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    # qs_product = Product.objects.filter(~Q(is_active=2)).order_by('kategori')
    susun = request.GET.get('sorting')
    if susun is False:
        qs_product = Product.objects.filter(~Q(is_active=2)).order_by('kategori')
    elif susun == 'newest':
        qs_product = Product.objects.filter(~Q(is_active=2)).order_by('date_created')
    elif susun == 'oldest':
        qs_product = Product.objects.filter(~Q(is_active=2)).order_by('-date_created')
    elif susun  == 'atoz':
        qs_product = Product.objects.filter(~Q(is_active=2)).order_by('namaproduct')
    elif susun == 'ztoa':
        qs_product = Product.objects.filter(~Q(is_active=2)).order_by('-namaproduct')
    else:
        qs_product = Product.objects.filter(~Q(is_active=2)).order_by('kategori')
        
    paginator = Paginator(qs_product, 12)
    page = request.GET.get('page',1)
    try:
        produk = paginator.page(page)
    except PageNotAnInteger:
        produk = paginator.page(page)
    except EmptyPage:
        produk = paginator.page(page)
    return render(request,'frontend/artwork.html', {
                                                    'title':'Artwork',
                                                    'kategori': KATEGORI,
                                                    'slider':SLIDER,
                                                    'produk':produk,
                                                        })

#detail product
def detailproduct(request, slug):
    KATEGORI = Kategori.objects.filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    qs_product = Product.objects.filter(slug=slug)
    # return HttpResponse(qs_product)
    if qs_product.count() == 0:
        redirect('notfoundpage')
    else:
        return render(request, 'frontend/detailproduct.html', {'title':'Detail Product',
                                                            'kategori': KATEGORI,
                                                            'slider':SLIDER,
                                                            'produk':Product.objects.get(slug=slug),
                                                            })

def notfound(request):
    KATEGORI = Kategori.objects.all().filter(~Q(is_active=2))
    SLIDER = Slider.objects.all().filter(~Q(is_active=2))
    return render(request, 'frontend/notfound.html', {'title':'Halaman Tidak Di Temukan'})

    