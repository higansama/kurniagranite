from .models import *
from rest_framework import serializers



class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('namamaterial', 'is_active', 'date_created', 'gambar1', 'gambar2', 'gambar3', 'gambar4', 'gambar5', 'date_updated')