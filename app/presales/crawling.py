import os
import re
import time
import urllib
import requests
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

from config.settings.base import MEDIA_ROOT
from presales.models import PreSale, PreSaleImage, Thema, Brand


def presaleCrawling():
    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    presaleMainList = [
            'https://www.dabangapp.com/sales-in-lots#/theme',
        # 'https://www.dabangapp.com/sales-in-lots#/brand'
    ]

    for main_url in presaleMainList:
        driver.get(main_url)
        if main_url == 'https://www.dabangapp.com/sales-in-lots#/theme':

            concept_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/p')

            # 테마분양 크롤링
            for index in range(len(concept_list)):
                try:
                    button = driver.find_element_by_xpath(
                        f'/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/p[{index+1}]')
                    # 테마 모델 생성
                    thema = driver.find_element_by_xpath(
                        f'/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/p[{index+1}]')
                    thema = thema.get_attribute('innerText')
                    print(thema)
                    thema_ins, __ = Thema.objects.get_or_create(
                        name=thema,
                    )

                    print(thema, '------------------------ thema')

                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(1)

                    brand = None
                    table_rows = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr')
                    for row_index, rows in enumerate(range(len(table_rows))):
                        button = driver.find_element_by_xpath(
                            f'/html/body/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr[{row_index+1}]')
                        driver.execute_script("arguments[0].click();", button)
                        driver.switch_to_window(driver.window_handles[1])
                        print(row_index + 1)
                        time.sleep(1)
                        # 페이지 크롤링 시작
                        status = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/span[1]')
                        status = status.get_attribute('innerText')
                        print('status >>', status)

                        term = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/span[2]')
                        term = term.get_attribute('innerText')
                        print('term>>>', term)

                        name = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/h1')
                        name = name.get_attribute('innerText')
                        print('name >>> ', name)

                        place = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/p')
                        place = place.get_attribute('innerText')
                        print('place >>>> ', place)

                        sales_type = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/div/div[2]/span')
                        sales_type = sales_type.get_attribute('innerText')
                        print('sales type >>>> ', sales_type)

                        sales_price = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[2]/p')
                        sales_price = sales_price.get_attribute('innerText')
                        print('sales price >>> ', sales_price)

                        total_citizen = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[1]/p[2]')
                        total_citizen = total_citizen.get_attribute('innerText')
                        print('total citizen >> ', total_citizen)

                        sales_citizen = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[2]/p[2]')
                        sales_citizen = sales_citizen.get_attribute('innerText')
                        print('sales_citizen >>>> ', sales_citizen)

                        min_max_floor = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[3]/p[2]')
                        min_max_floor = min_max_floor.get_attribute('innerText')
                        print('min_max_floor >>> ', min_max_floor)

                        complex_scale = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[4]/p[2]')
                        complex_scale = complex_scale.get_attribute('innerText')
                        print('complex_sclae >> ', complex_scale)

                        # 디테일부분 시

                        detail_type = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[1]')
                        detail_type = detail_type.get_attribute('innerText')
                        print('detail_type >>> ', detail_type)

                        constraint = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[1]')
                        constraint = constraint.get_attribute('innerText')
                        print('constraint >>', constraint)

                        area = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[3]/td[1]')
                        area = area.get_attribute('innerText')
                        print('area >>>', area)

                        supply_type = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[2]')
                        supply_type = supply_type.get_attribute('innerText')
                        print('supply_type >>', supply_type)

                        constraint_area = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[2]')
                        constraint_area = constraint_area.get_attribute('innerText')
                        print('constraint 공급 제한 지역 >>', constraint_area)

                        recruit = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[3]/td[2]')
                        recruit = recruit.get_attribute('innerText')
                        print('recruit >>', recruit)

                        builder = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[3]')
                        builder = builder.get_attribute('innerText')
                        print('builder >>', builder)

                        max_price = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[3]')
                        max_price = max_price.get_attribute('innerText')
                        print('max_price >>> ', max_price)

                        moveIn = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[3]/td[3]')
                        moveIn = moveIn.get_attribute('innerText')
                        print('move In >>>', moveIn)

                        developer = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[4]')
                        developer = developer.get_attribute('innerText')
                        print('developer >>', developer)

                        constraint_term = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[4]')
                        constraint_term = constraint_term.get_attribute('innerText')
                        print('constraint_term >>>', constraint_term)

                        div_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[4]/div/div/div')

                        # 가격 정보

                        try:
                            detail_price = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div[6]/div[1]/div/ul/li[1]/div/p[2]')
                            detail_price = detail_price.get_attribute('innerText')
                            print('detail_price >>', detail_price)
                            price_pyeong = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div[6]/div[1]/div/ul/li[2]/div/p[2]')
                            price_pyeong = price_pyeong.get_attribute('innerText')
                            print('price_pyeong>>', price_pyeong)

                            aver_price = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div[6]/div[1]/div/ul/li[2]/div/p[3]'
                            )
                            aver_price = aver_price.get_attribute('innerText')
                            print('aver_price', aver_price)

                        except NoSuchElementException:
                            detail_price = None
                            price_pyeong = None
                            aver_price = None
                            print(detail_price, price_pyeong, aver_price)

                        pre_ins, __ = PreSale.objects.get_or_create(
                            thema=thema_ins,
                            brand=brand,
                            status=status,
                            term=term,
                            name=name,
                            place=place,
                            sales_type=sales_type,
                            sales_price=sales_price,
                            total_citizen=total_citizen,
                            sales_citizen=sales_citizen,
                            min_max_floor=min_max_floor,
                            complex_scale=complex_scale,

                            detail_type=detail_type,
                            constraint=constraint,
                            area=area,
                            supply_type=supply_type,
                            constraint_area=constraint_area,
                            recruit=recruit,
                            builder=builder,
                            max_price=max_price,
                            moveIn=moveIn,
                            developer=developer,
                            constraint_term=constraint_term,

                            detail_price=detail_price,
                            price_pyeong=price_pyeong,
                            aver_price=aver_price
                        )

                        print(pre_ins, thema_ins.name, '가 생성되었습니다.===================================')

                        # 이미지 생성
                        preSalesImageList = []

                        for i, url in enumerate(div_list):
                            try:
                                cls_name = url.get_attribute('class')
                                cls_name = cls_name.split(' ')
                                cls_name = cls_name[1]
                                photo = driver.execute_script(
                                    f'return window.getComputedStyle(document.querySelector(".{cls_name}"),":after").getPropertyValue("background")')
                                recommend_image = re.findall(r'"(.*?)"', photo)
                                preSalesImageList.append(recommend_image[0])
                            except IndexError:
                                pass

                        for index, image in enumerate(preSalesImageList):
                            try:
                                PRESALE_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/complex{pre_ins.pk}/')
                                if not os.path.exists(PRESALE_IMAGE_DIR):
                                    os.makedirs(PRESALE_IMAGE_DIR, exist_ok=True)

                                image_save_name = os.path.join(PRESALE_IMAGE_DIR, f'{index}.jpg')
                                urllib.request.urlretrieve(image, image_save_name)
                                f = open(os.path.join(PRESALE_IMAGE_DIR, f'{index}.jpg'), 'rb')
                                preImage_ins, __ = PreSaleImage.objects.get_or_create(
                                    image=File(f),
                                    presale=pre_ins,
                                )
                                print(preImage_ins, '가 생성 되었습니다 ###################')
                            except FileExistsError:
                                print('이미 존재하는 파일')

                        # 창 닫고 테마 리스트로 이동
                        driver.close()
                        driver.switch_to_window(driver.window_handles[0])

                    print('--------')
                except NoSuchElementException:
                    pass

        else:
            for url in presaleMainList:
                print(url)
                driver.get(url)
                brand_name_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/div/div')
                for index in range(len(brand_name_list)):
                    print(f'{index+1}')
                    print(f'/html/body/div[1]/div/div[2]/div/div/div[1]/div/div[{index+1}]')
                    button = driver.find_element_by_xpath(
                        f'/html/body/div[1]/div/div[2]/div/div/div[1]/div/div[{index+1}]')
                    brand = button.get_attribute('innerText')
                    print('brand >>', brand)

                    brand_ins, __ = Brand.objects.get_or_create(
                        name=brand
                    )

                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(1)
                    table_rows = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr')
                    for row_index, rows in enumerate(range(len(table_rows))):
                        button = driver.find_element_by_xpath(
                            f'/html/body/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr[{row_index+1}]')
                        driver.execute_script("arguments[0].click();", button)
                        driver.switch_to_window(driver.window_handles[1])
                        time.sleep(1)
                        thema_ins = None
                        #             페이지 크롤링 시작
                        status = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/span[1]')
                        status = status.get_attribute('innerText')
                        print('status >>', status)

                        term = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/span[2]')
                        term = term.get_attribute('innerText')
                        print('term>>>', term)

                        name = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/h1')
                        name = name.get_attribute('innerText')
                        print('name >>> ', name)

                        place = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[1]/p')
                        place = place.get_attribute('innerText')
                        print('place >>>> ', place)

                        sales_type = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/div/div[2]/span')
                        sales_type = sales_type.get_attribute('innerText')
                        print('sales type >>>> ', sales_type)

                        sales_price = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div[2]/p')
                        sales_price = sales_price.get_attribute('innerText')
                        print('sales price >>> ', sales_price)

                        total_citizen = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[1]/p[2]')
                        total_citizen = total_citizen.get_attribute('innerText')
                        print('total citizen >> ', total_citizen)

                        sales_citizen = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[2]/p[2]')
                        sales_citizen = sales_citizen.get_attribute('innerText')
                        print('sales_citizen >>>> ', sales_citizen)

                        min_max_floor = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[3]/p[2]')
                        min_max_floor = min_max_floor.get_attribute('innerText')
                        print('min_max_floor >>> ', min_max_floor)

                        complex_scale = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[1]/div/ul/li[4]/p[2]')
                        complex_scale = complex_scale.get_attribute('innerText')
                        print('complex_sclae >> ', complex_scale)

                        # 디테일부분 시

                        detail_type = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[1]')
                        detail_type = detail_type.get_attribute('innerText')
                        print('detail_type >>> ', detail_type)

                        constraint = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[1]')
                        constraint = constraint.get_attribute('innerText')
                        print('constraint >>', constraint)

                        area = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[3]/td[1]')
                        area = area.get_attribute('innerText')
                        print('area >>>', area)

                        supply_type = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[2]')
                        supply_type = supply_type.get_attribute('innerText')
                        print('supply_type >>', supply_type)

                        constraint_area = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[2]')
                        constraint_area = constraint_area.get_attribute('innerText')
                        print('constraint 공급 제한 지역 >>', constraint_area)

                        recruit = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[3]/td[2]')
                        recruit = recruit.get_attribute('innerText')
                        print('recruit >>', recruit)

                        builder = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[3]')
                        builder = builder.get_attribute('innerText')
                        print('builder >>', builder)

                        max_price = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[3]')
                        max_price = max_price.get_attribute('innerText')
                        print('max_price >>> ', max_price)

                        moveIn = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[3]/td[3]')
                        moveIn = moveIn.get_attribute('innerText')
                        print('move In >>>', moveIn)

                        developer = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[1]/td[4]')
                        developer = developer.get_attribute('innerText')
                        print('developer >>', developer)

                        constraint_term = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div[3]/div/table/tbody/tr[2]/td[4]')
                        constraint_term = constraint_term.get_attribute('innerText')
                        print('constraint_term >>>', constraint_term)

                        div_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[4]/div/div/div')

                        # 가격 정보

                        try:
                            detail_price = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div[6]/div[1]/div/ul/li[1]/div/p[2]')
                            detail_price = detail_price.get_attribute('innerText')
                            print('detail_price >>', detail_price)
                            price_pyeong = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div[6]/div[1]/div/ul/li[2]/div/p[2]')
                            price_pyeong = price_pyeong.get_attribute('innerText')
                            print('price_pyeong>>', price_pyeong)

                            aver_price = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div[6]/div[1]/div/ul/li[2]/div/p[3]'
                            )
                            aver_price = aver_price.get_attribute('innerText')
                            print('aver_price', aver_price)

                        except NoSuchElementException:
                            detail_price = None
                            price_pyeong = None
                            aver_price = None
                            print(detail_price, price_pyeong, aver_price)

                        pre_ins, __ = PreSale.objects.get_or_create(
                            thema=thema_ins,
                            brand=brand_ins,
                            status=status,
                            term=term,
                            name=name,
                            place=place,
                            sales_type=sales_type,
                            sales_price=sales_price,
                            total_citizen=total_citizen,
                            sales_citizen=sales_citizen,
                            min_max_floor=min_max_floor,
                            complex_scale=complex_scale,

                            detail_type=detail_type,
                            constraint=constraint,
                            area=area,
                            supply_type=supply_type,
                            constraint_area=constraint_area,
                            recruit=recruit,
                            builder=builder,
                            max_price=max_price,
                            moveIn=moveIn,
                            developer=developer,
                            constraint_term=constraint_term,

                            detail_price=detail_price,
                            price_pyeong=price_pyeong,
                            aver_price=aver_price
                        )

                        print(pre_ins,'가 생성되었습니다.===================================')

                        # 이미지 생성
                        preSalesImageList = []

                        for i, url in enumerate(div_list):
                            try:
                                cls_name = url.get_attribute('class')
                                cls_name = cls_name.split(' ')
                                cls_name = cls_name[1]
                                photo = driver.execute_script(
                                    f'return window.getComputedStyle(document.querySelector(".{cls_name}"),":after").getPropertyValue("background")')
                                recommend_image = re.findall(r'"(.*?)"', photo)
                                preSalesImageList.append(recommend_image[0])
                            except IndexError:
                                pass

                        for index, image in enumerate(preSalesImageList):
                            try:
                                PRESALE_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/presale{pre_ins.pk}/')
                                if not os.path.exists(PRESALE_IMAGE_DIR):
                                    os.makedirs(PRESALE_IMAGE_DIR, exist_ok=True)

                                image_save_name = os.path.join(PRESALE_IMAGE_DIR, f'{index}.jpg')
                                urllib.request.urlretrieve(image, image_save_name)
                                f = open(os.path.join(PRESALE_IMAGE_DIR, f'{index}.jpg'), 'rb')
                                preImage_ins, __ = PreSaleImage.objects.get_or_create(
                                    image=File(f),
                                    presale=pre_ins,
                                )
                                print(preImage_ins, '가 생성 되었습니다 ###################')
                            except FileExistsError:
                                print('이미 존재하는 파일')
                        driver.close()
                        driver.switch_to_window(driver.window_handles[0])
                    print('--------')
