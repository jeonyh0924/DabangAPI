from rest_framework import serializers

from presales.models import PreSale, Brand, Thema, PreSaleImage


class BrandSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', ]


class ThemaSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Thema
        fields = ['name', ]


class PreSaleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreSaleImage
        fields = ['image', ]


class PreSaleSerializer(serializers.ModelSerializer):
    brand = BrandSerialzier()
    thema = ThemaSerialzier()
    image = serializers.StringRelatedField(source='presaleimage_set', many=True, )
    list = serializers.SerializerMethodField()

    class Meta:
        model = PreSale
        fields = ('__all__')

    def get_list(self, obj):
        import random
        pk_list = []
        while True:
            max_id = PreSale.objects.all()
            max_id = len(max_id)
            pk = random.randint(1, max_id)
            ins = PreSale.objects.get(pk=pk)
            if ins.pk in pk_list:
                pass
            else:
                if obj.pk == ins.pk:
                    pass
                else:
                    pk_list.append(ins.pk)
            if len(pk_list) >= 4:
                break
        return pk_list


class PreSaleTinySerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField(source='presaleimage_set', many=True, )

    class Meta:
        model = PreSale
        fields = [
            'id',
            'status',
            'detail_type',
            'supply_type',
            'name',
            'place',
            'term',
            'image',
        ]
