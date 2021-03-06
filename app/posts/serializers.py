from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
# from members.serializers import UserSerializer
from .models import PostRoom, PostImage, Broker, MaintenanceFee, RoomOption, PostAddress, RoomSecurity, SalesForm, \
    OptionItem, SecuritySafetyFacilities, ComplexInformation, ComplexImage, RecommendComplex, PostLike, ComplexLike

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'password',
            'username',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        return make_password(value)


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceFee
        fields = (
            'pk', 'postRoom', 'admin', 'totalFee',
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionItem
        fields = (
            'name',
        )


class SecuritySafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySafetyFacilities
        fields = (
            'pk',
            'name',
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = (
            'pk', 'loadAddress', 'detailAddress',
        )


class SalesFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesForm
        fields = (
            'pk',
            'type',
            'depositChar',
            'monthlyChar',
            'depositInt',
            'monthlyInt',
        )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )


class RecommendComplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendComplex
        fields = '__all__'


class ComplexTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexInformation
        fields = [
            'pk',
            'complexName',
        ]


class ComplexImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexImage
        field = 'image'


class ComplexInformationSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField(source='compleximage_set', many=True, read_only=True)
    list = serializers.SerializerMethodField()
    countPost = serializers.SerializerMethodField(read_only=True)

    def get_countPost(self, obj):
        return obj.postroom_set.count()

    def get_list(self, obj):
        import random

        pk_list = []
        while True:
            max_id = ComplexInformation.objects.all()
            max_id = len(max_id)
            pk = random.randint(1, max_id)
            ins = ComplexInformation.objects.get(pk=pk)
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

    class Meta:
        model = ComplexInformation
        fields = (
            'pk',
            'complexName',
            'buildDate',
            'totalCitizen',
            'personalPark',
            'totalNumber',
            'heatingSystem',
            'minMaxFloor',
            'buildingType',
            'constructionCompany',
            'fuel',
            'complexType',
            'floorAreaRatio',
            'dryWasteRate',
            'complexSale',
            'complexPrice',
            'areaSale',
            'areaPrice',
            'image',
            'list',
            'countPost',
        )

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        # broker = re
        complex_ins = ComplexInformation.objects.create(**validated_data)
        for image_data in images_data.getlist('image'):
            ComplexImage.objects.create(image=image_data, complex=complex_ins)
        return complex_ins


class BrokerSerializer(serializers.ModelSerializer):
    pkList = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='postroom_set')

    class Meta:
        model = Broker
        fields = (
            'pk', 'companyName', 'address', 'managerName', 'tel', 'image', 'companyNumber', 'brokerage',
            'dabangCreated_at', 'successCount', 'pkList'
        )


class PostListSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer(read_only=True, )
    management_set = serializers.StringRelatedField(source='management', many=True, read_only=True)
    option_set = serializers.StringRelatedField(source='option', many=True, read_only=True)
    securitySafety_set = serializers.StringRelatedField(source='securitySafety', many=True, read_only=True)
    address = AddressSerializer(read_only=True, allow_null=True)
    salesForm = SalesFormSerializer(read_only=True)
    postimage = serializers.StringRelatedField(source='images', many=True, read_only=True, )
    complex = ComplexInformationSerializer(read_only=True, )

    class Meta:
        model = PostRoom
        fields = [
            'pk',
            'broker',
            'type',
            'name',
            'description',
            'address',
            'lng',
            'lat',
            'salesForm',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'management_set',
            'parkingDetail',
            'parkingTF',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'option_set',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'totalCitizen',
            'totalPark',
            'complete',
            'securitySafety_set',
            'postimage',
            'complex',
        ]

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        post_ins = PostRoom.objects.create(**validated_data)
        for image_data in images_data.getlist('image'):
            PostImage.objects.create(image=image_data, post=post_ins)
        return post_ins


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = [
            'post',
            'user',
        ]


class ComplexLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexLike
        fields = [
            'complexs',
            'user',
        ]


class PostLikeUserSerializer(serializers.ModelSerializer):
    post = PostListSerializer()

    class Meta:
        model = PostLike
        fields = [
            'post',
        ]


class ComplexLikeUserSerializer(serializers.ModelSerializer):
    complexs = ComplexInformationSerializer()

    class Meta:
        model = ComplexLike
        fields = [
            'complexs',
        ]


class PostTinySerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True, allow_null=True)
    salesForm = SalesFormSerializer(read_only=True)
    postimage = serializers.StringRelatedField(source='images', many=True)
    complex = ComplexTinySerializer(read_only=True, )
    optionSet = serializers.StringRelatedField(source='option', many=True, read_only=True)

    class Meta:
        model = PostRoom
        fields = [
            'pk',
            'type',
            'name',
            'supplyAreaInt',
            'description',
            'address',
            'lng',
            'lat',
            'salesForm',
            'pet',
            'elevator',
            'veranda',
            'depositLoan',
            'postimage',
            'complex',
            'areaChar',
            'floor',
            'optionSet',

        ]


class PostCreateSerializer(serializers.ModelSerializer):
    complex = ComplexInformationSerializer(read_only=True, )
    salesForm = SalesFormSerializer(read_only=True, )
    author = UserSerializer(read_only=True, )
    broker = BrokerSerializer(read_only=True, )
    postImage = PostImageSerializer(source='post_set', many=True, read_only=True)
    address = AddressSerializer(read_only=True, allow_null=True)
    option = OptionSerializer(many=True, read_only=True, )
    securitySafety = SecuritySafetySerializer(many=True, read_only=True, )

    class Meta:
        model = PostRoom
        fields = [
            'pk',
            'author',
            'broker',
            'complex',
            'salesForm',
            'address',
            'type',
            'description',
            'lat',
            'lng',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'parkingDetail',
            'parkingTF',
            'parkingPay',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'totalCitizen',
            'totalPark',
            'complete',
            'option',
            'securitySafety',
            'postImage',

        ]

    def create(self, validated_data):
        salesform_ins = SalesForm.objects.create(
            type=self.context['request'].data.get('salesFormType'),
            depositChar=self.context['request'].data.get('depositChar'),
            monthlyChar=self.context['request'].data.get('monthlyChar'),
            depositInt=self.context['request'].data.get('depositInt'),
            monthlyInt=self.context['request'].data.get('monthlyInt'),
        )

        add_ins, __ = PostAddress.objects.get_or_create(
            loadAddress=self.context['request'].data.get('loadAddress'),
            detailAddress=self.context['request'].data.get('detailAddress')
        )

        broker = Broker.objects.get(pk=1)
        user = User.objects.first()
        post = PostRoom.objects.create(
            **validated_data,
            author=user,
            broker=broker,
            salesForm=salesform_ins,
            address=add_ins,
        )

        options = self.context['request'].data.get('options')
        if options:
            options = options.split(',')
            for option in options:
                option_ins = OptionItem.objects.get(name=option)
                post.option.add(option_ins)
        security_safetys = self.context['request'].data.get('security_safetys')
        if security_safetys:
            security_safetys = security_safetys.split(',')
            for ss in security_safetys:
                ss_ins = SecuritySafetyFacilities.objects.get(name=ss)
                post.securitySafety.add(ss_ins)

        images_data = self.context['request'].FILES
        for image_data in images_data.getlist('image'):
            PostImage.objects.create(post=post, image=image_data)
        return post


class PostTestSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = PostRoom
        fields = ['pk', 'type', 'images']

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        post = PostRoom.objects.create(**validated_data)
        for image_data in images_data.getlist('image'):
            PostImage.objects.create(post=post, image=image_data)
        return post
