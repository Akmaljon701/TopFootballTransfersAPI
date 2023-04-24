from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import *

class ClubSerializer(ModelSerializer):
    transfer_narxi = SerializerMethodField()
    class Meta:
        model = Club
        fields = '__all__'

    def get_transfer_narxi(self, obj):
        return obj.sotuvlari.aggregate(sum=models.Sum('narxi')).get('sum')

class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

    def to_representation(self, instance):
        transfer = super().to_representation(instance)
        transfer['divergence(%)'] = abs(instance.narxi - instance.tax_narx) * 100 // instance.narxi
        return transfer