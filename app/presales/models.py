from django.db import models


def presales_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


# Create your models here.

class Thema(models.Model):
    name = models.CharField('테마 명', max_length=30)

    def __str__(self):
        return '{}'.format(self.name)


class Brand(models.Model):
    name = models.CharField('브랜드 명', max_length=30)

    def __str__(self):
        return '{}'.format(self.name)


class PreSale(models.Model):
    thema = models.ForeignKey(
        Thema,
        on_delete=models.CASCADE,
        null=True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
    )
    status = models.CharField('분양 예정', max_length=10)
    term = models.CharField('모집 공고', max_length=30)
    name = models.CharField('단지 명', max_length=40)
    place = models.CharField('장소', max_length=25)
    sales_type = models.CharField('판매 유형', max_length=10)
    sales_price = models.CharField('분양 가격', max_length=40)
    total_citizen = models.CharField('총 세대수', max_length=20)
    sales_citizen = models.CharField('분양 세대 수', max_length=20)
    min_max_floor = models.CharField('최저-최고 층', max_length=40)
    complex_scale = models.CharField('단지 규모', max_length=10)

    detail_type = models.CharField('건물 유형', max_length=10)
    constraint = models.CharField('전매 가능 여부', max_length=15)
    area = models.CharField('전용 면적', max_length=30)
    supply_type = models.CharField('공급 유형', max_length=10)
    constraint_area = models.CharField('규제 지역', max_length=10)
    recruit = models.CharField('모집 공고일', max_length=20)
    builder = models.CharField('건설사', max_length=20)
    max_price = models.CharField('분양가 상한제', max_length=10)
    moveIn = models.CharField('입주 예정일', max_length=20)
    developer = models.CharField('시행사', max_length=40)
    constraint_term = models.CharField('규제 기간', max_length=40)

    detail_price = models.CharField('분양가', max_length=20, null=True, )
    price_pyeong = models.CharField('평당가', max_length=20, null=True, )
    aver_price = models.CharField('지역 평균가', max_length=50, null=True, )

    @staticmethod
    def crawling():
        from presales.crawling import presaleCrawling
        presaleCrawling()


class PreSaleImage(models.Model):
    presale = models.ForeignKey(
        PreSale,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=presales_image_path,
        null=True,
    )

    def __str__(self):
        return '{}'.format(self.image)
