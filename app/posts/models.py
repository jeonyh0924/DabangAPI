from django.db import models

from config import settings

from imagekit.models import ProcessedImageField


def post_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def complex_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def recommend_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def security_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def broker_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def uploadpost_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


class PostRoom(models.Model):
    broker = models.ForeignKey(
        'posts.Broker',
        on_delete=models.SET_NULL,
        null=True,
    )
    complex = models.ForeignKey(
        'ComplexInformation',
        on_delete=models.CASCADE,
        verbose_name='단지',
        null=True,
    )
    type = models.CharField('매물 종류', max_length=10, null=True, )
    description = models.TextField(max_length=500, verbose_name='설명', null=True, )
    address = models.ForeignKey(
        'posts.PostAddress',
        on_delete=models.CASCADE, null=True,
    )
    salesForm = models.OneToOneField(
        'posts.SalesForm',
        on_delete=models.CASCADE, null=True, related_name='salesform_set',
    )
    # 위도 경도
    lat = models.FloatField('x축', null=True, )
    lng = models.FloatField('y축', null=True, )

    floor = models.CharField(null=True, verbose_name='층 수', max_length=5)
    totalFloor = models.CharField(null=True, verbose_name='건물 층 수', max_length=5)
    areaChar = models.CharField(verbose_name='문자형 전용 면적', max_length=20, null=True, )
    supplyAreaInt = models.IntegerField(verbose_name='정수형 공급 면적', null=True, )
    supplyAreaChar = models.CharField(verbose_name='문자형 공급 면적', max_length=10, null=True, )
    shortRent = models.NullBooleanField('단기임대', default=None, )
    management = models.ManyToManyField(
        'posts.AdministrativeDetail',
        through='MaintenanceFee',
    )

    parkingDetail = models.CharField(verbose_name='주차 비용', null=True, max_length=10)
    parkingTF = models.NullBooleanField('주차 가능 유무', default=None)
    parkingPay = models.FloatField('주차 비용', null=True, )

    living_expenses = models.CharField('생활비', null=True, max_length=15, )
    living_expenses_detail = models.CharField('생활비 항목', null=True, max_length=20, )

    moveInChar = models.CharField('크롤링용 입주날짜', null=True, max_length=10)
    moveInDate = models.DateTimeField(verbose_name='입주 가능 날짜', null=True, )
    #
    option = models.ManyToManyField('OptionItem', through='RoomOption', verbose_name='옵션 항목')
    heatingType = models.CharField('난방 종류', max_length=10, null=True, )

    pet = models.NullBooleanField('반려동물', default=None)
    elevator = models.NullBooleanField('엘레베이터', default=None)
    builtIn = models.NullBooleanField('빌트인', default=None)
    veranda = models.NullBooleanField('베란다/ 발코니', default=None)
    depositLoan = models.NullBooleanField('전세 자금 대출', default=None)
    totalCitizen = models.CharField('총 세대 수', max_length=10, null=True, )
    totalPark = models.CharField('세대당 주차 대수', max_length=10, null=True, )
    complete = models.CharField('준공 년 월', max_length=10, null=True, )

    securitySafety = models.ManyToManyField(
        'posts.SecuritySafetyFacilities',
        through='RoomSecurity',
    )

    @staticmethod
    def project_crawling_start():
        from posts.crawling.postFind import postFind
        postFind()


class PostAddress(models.Model):
    loadAddress = models.CharField(max_length=50, null=True, )
    detailAddress = models.CharField(max_length=30, null=True, )


class SalesForm(models.Model):
    type = models.CharField(max_length=10, verbose_name='매물 종류', )
    depositChar = models.CharField(null=True, verbose_name='문자형 매매-보증금', max_length=10)  # 보증금
    monthlyChar = models.CharField(null=True, verbose_name='문자형 월세', max_length=10)  # 월세
    depositInt = models.IntegerField('정수형 매매-보증금', null=True, )
    monthlyInt = models.IntegerField('정수형 월세', null=True, )

    @staticmethod
    def start():
        type_list = ['매매', '전세', '월세']
        for i in type_list:
            SalesForm.objects.create(
                type=i,
            )

    @staticmethod
    def make_obj():
        SalesForm.objects.create()


class MaintenanceFee(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE,
                                 related_name='management_set')
    admin = models.ForeignKey('posts.AdministrativeDetail', verbose_name='포함 항목', on_delete=models.CASCADE, null=True, )
    totalFee = models.FloatField(verbose_name='관리비 합계', null=True, )


# 관리비 포함 항목
class AdministrativeDetail(models.Model):
    name = models.CharField(max_length=10, verbose_name='포함 항목 물품')

    def __str__(self):
        return '{}'.format(self.name)


class OptionItem(models.Model):
    name = models.CharField('옵션 항목 아이템', max_length=10, )
    image = models.ImageField('옵션 이미지', null=True, )

    def __str__(self):
        return '{}'.format(self.name)


class SecuritySafetyFacilities(models.Model):
    name = models.CharField('보안/안전 시설 아이템', max_length=10, null=True)
    image = models.ImageField('시설 이미지', null=True, upload_to=security_image_path, )

    def __str__(self):
        return '{}'.format(self.name)


class PostLike(models.Model):
    post = models.ForeignKey('posts.PostRoom', on_delete=models.CASCADE, )
    user = models.ForeignKey(
        settings.base.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class RoomOption(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE,
                                 related_name='option_set')
    option = models.ForeignKey('OptionItem', verbose_name='해당 옵션', on_delete=models.CASCADE,
                               related_name='optionname_set')
    created_at = models.DateTimeField(auto_now_add=True, )


class RoomSecurity(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE,
                                 related_name='securitySafety_set')
    security = models.ForeignKey('posts.SecuritySafetyFacilities', verbose_name='보안 안전 시설', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True, )


class Broker(models.Model):
    companyName = models.CharField('회사 명', max_length=30, null=True, )
    address = models.CharField('주소', max_length=50, null=True, )
    managerName = models.CharField('중개인', max_length=30, null=True, )
    tel = models.CharField('전화번호', max_length=13, null=True, )
    image = models.ImageField('이미지', upload_to=broker_image_path, null=True, )
    companyNumber = models.CharField('사업자 번호', max_length=20, null=True, )
    brokerage = models.CharField('중개등록번호', max_length=30, null=True, )
    dabangCreated_at = models.CharField('다방 가입일', max_length=20, null=True, )
    successCount = models.CharField('거래 성공 횟수', max_length=20, null=True, )


class PostImage(models.Model):
    image = models.ImageField(upload_to=post_image_path, verbose_name='방 이미지', null=True, )
    post = models.ForeignKey(
        'posts.postRoom',
        verbose_name='해당 게시글',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}'.format(self.image)


class ComplexInformation(models.Model):
    complexName = models.CharField('단지 이름', max_length=30, null=True, )
    buildDate = models.CharField('설립 날짜', max_length=20, null=True, )
    totalCitizen = models.CharField('총 세대 수', max_length=20, null=True, )
    personalPark = models.CharField('주차 대수', max_length=10, null=True, )
    totalNumber = models.CharField('총 동 수', max_length=10, null=True, )
    heatingSystem = models.CharField('난방 방식', max_length=15, null=True, )
    minMaxFloor = models.CharField('최저-최고 층', max_length=10, null=True, )
    buildingType = models.CharField('건물 유형', max_length=10, null=True, )
    constructionCompany = models.CharField('건설사', max_length=30, null=True, )
    fuel = models.CharField('연로', max_length=10, null=True, )
    complexType = models.CharField('단지 타입', max_length=10, null=True, )
    floorAreaRatio = models.CharField('용적률', max_length=10, null=True, )
    dryWasteRate = models.CharField('건폐율', max_length=10, null=True, )
    complexSale = models.CharField('단지 평당가 매매 ', max_length=10, null=True, )
    complexPrice = models.CharField('단지 평당가 전세 ', max_length=10, null=True, )
    areaSale = models.CharField('이 지역 평당가 매매', max_length=30, null=True, )
    areaPrice = models.CharField('이 지역 평당가 전세', max_length=30, null=True, )

    def __str__(self):
        return f'{self.complexName}'


class ComplexImage(models.Model):
    image = models.ImageField(upload_to=complex_image_path, verbose_name='방 이미지', null=True, )
    complex = models.ForeignKey(
        'posts.ComplexInformation',
        verbose_name='단지 정보',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}'.format(self.image)


class RecommendComplex(models.Model):
    complex = models.ForeignKey(ComplexInformation, verbose_name='단지', on_delete=models.CASCADE, )
    image = models.ImageField('추천 단지 이미지', upload_to=recommend_image_path, null=True, )
    name = models.CharField('추천 단지 명', null=True, max_length=30, )
    type = models.CharField('추천 단지 아파트 타입', null=True, max_length=20, )
    totalCitizen = models.CharField('추천 단지 총 세대 수', null=True, max_length=30, )
    buildDate = models.CharField('추천 단지 설립일자', null=True, max_length=20, )
    address = models.CharField('추천 단지 주소', null=True, max_length=20, )
    link = models.CharField('추천 단지 링크', max_length=100, null=True, )
