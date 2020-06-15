import json
import os
import re
import time
import urllib

import requests
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

from config import settings
from config.settings.base import MEDIA_ROOT
from members.models import SocialLogin
from posts.crawling.find_urls import find_apartment_urls, find_urls

from ..models import SalesForm, PostAddress, SecuritySafetyFacilities, OptionItem, \
    MaintenanceFee, RoomOption, RoomSecurity, PostRoom, Broker, PostImage, AdministrativeDetail, ComplexInformation, \
    ComplexImage, RecommendComplex

KAKAO_APP_ID = settings.base.KAKAO_APP_ID


def postFind():
    POSTS_DIR = os.path.join(MEDIA_ROOT, '.posts')

    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR, exist_ok=True)

    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    SocialLogin.start()
    # 다방 성수동 매물 url
    # url_all_list = find_apartment_urls()
    # print('아파트 단지 url', url_all_list)
    # officetels = find_urls()
    # url_all_list += officetels
    # print('오피스텔 매물', officetels)
    url_all_list = [
        # 'https://www.dabangapp.com/room/5ee480b9d7e0b95825bce292',
        # 'https://www.dabangapp.com/room/5ee480a84811734cf8f5a116',
        # 'https://www.dabangapp.com/room/5ee480a1418a3e5ce125ee73',
        # 'https://www.dabangapp.com/room/5ecd0375f543a315d6ade05e',
        # 'https://www.dabangapp.com/room/5ee480bbfe59d35825a9b953',
        # 'https://www.dabangapp.com/room/5ee480bc56eb7b4cf8fbb6f8',
        # 'https://www.dabangapp.com/room/5ed47b7d5eb7273021746fe8',
        # 'https://www.dabangapp.com/room/5ee480a689bfe1531f6d4bb0',
        # 'https://www.dabangapp.com/room/5eb36982f6fa2242e66e3de6',
        # 'https://www.dabangapp.com/room/5ee480aeaedd43531f00edd3',
        # 'https://www.dabangapp.com/room/5ee480b5c0652d438821236a',
        # 'https://www.dabangapp.com/room/5ee480adff01cc4dbc059904',
        # 'https://www.dabangapp.com/room/5ee074f9602c5856b5fcac42',
        # 'https://www.dabangapp.com/room/5ee480b3bfb18a531f30fecb',
        # 'https://www.dabangapp.com/room/5ee480b1ca95c243884502c5',
        # 'https://www.dabangapp.com/room/5ecb4883b0b6a90c653f1103',
        # 'https://www.dabangapp.com/room/5ee480b2dd8bb85825ddfb91',
        # 'https://www.dabangapp.com/room/5ee480b645ed61438826d335',
        # 'https://www.dabangapp.com/room/5ed60c8c6cc0ee78595c7bcb',
        # 'https://www.dabangapp.com/room/5ed44ef91d3ad910d0a0df2d',
        # 'https://www.dabangapp.com/room/5ed45371d1591662d23cae1a',
        # 'https://www.dabangapp.com/room/5ec880612326375e750f8a42',
        # 'https://www.dabangapp.com/room/5ed9a68ebb7af6280a1c9252',
        # 'https://www.dabangapp.com/room/5ed47c6816aa3a68bc8e40ac',
        # 'https://www.dabangapp.com/room/5ee04ad1b8d6780e12451a7a',
        # 'https://www.dabangapp.com/room/5ee06cc82a80ba2ddf800588',
        # 'https://www.dabangapp.com/room/5ecb0e5da7f7155e8bf3e85d',
        # 'https://www.dabangapp.com/room/5edf10d3afa4444c13c59a0a',
        # 'https://www.dabangapp.com/room/5edd993f5d62d76b0f48ef30',
        # 'https://www.dabangapp.com/room/5ed9b5ff25fbb555ad09fa27',
        # 'https://www.dabangapp.com/room/5ee2d54d65c3a2225c26d160',
        # 'https://www.dabangapp.com/room/5edf0a348aa9a63eb1a18fe4',
        # 'https://www.dabangapp.com/room/5ee1a8f34f15bc62deea096a',
        # 'https://www.dabangapp.com/room/5ed5fd83ca5da13a230a7267',
        # 'https://www.dabangapp.com/room/5ecb8582328bad5313674da6',
        # 'https://www.dabangapp.com/room/5edd95259688d27ff3a32b35',
        # 'https://www.dabangapp.com/room/5ec7a9da4b32f91de82a97f7',
        # 'https://www.dabangapp.com/room/5ed9d76e33b9096e582fcc8b',
        # 'https://www.dabangapp.com/room/5edd971dbfd4d237f7384b8a',
        # 'https://www.dabangapp.com/room/5ededdf9e3b102473e0d1962',
        # 'https://www.dabangapp.com/room/5ede3748a68c0e08194f5d19',
        # 'https://www.dabangapp.com/room/5eddcc7a660d45025f6fb511',
        # 'https://www.dabangapp.com/room/5ee1a6227001342861e0b435',
        # 'https://www.dabangapp.com/room/5ee061914a171c710cdc4df5',
        # 'https://www.dabangapp.com/room/5ec910739b21ea231d4d0252',
        # 'https://www.dabangapp.com/room/5ed9bef808ed830f3d245df6',
        # 'https://www.dabangapp.com/room/5ee2efa74641d035b1aada80',
        # 'https://www.dabangapp.com/room/5ee09f4d9e5e45270a8094ba',
        # 'https://www.dabangapp.com/room/5edf39ef216aec1a82b75e67',
        # 'https://www.dabangapp.com/room/5ee09d8ca5624a0db790ff32',
        # 'https://www.dabangapp.com/room/5ede0a9f736afd3533112cdd',
        # 'https://www.dabangapp.com/room/5ed9ccb7e55281201e1fd89b',
        # 'https://www.dabangapp.com/room/5ed4566e788ed611b9887164',
        # 'https://www.dabangapp.com/room/5ece10799747c12812cb5c29',
        # 'https://www.dabangapp.com/room/5ecb1bfbba1e125e0d6b4d9a',
        # 'https://www.dabangapp.com/room/5ec61a9d2aa8424d3faa75f6',
        # 'https://www.dabangapp.com/room/5ed460e8950de1189d0b4882',
        # 'https://www.dabangapp.com/room/5ede0788a21eeb7937260990',
        # 'https://www.dabangapp.com/room/5ebe5612cf09017213b37e45',
        # 'https://www.dabangapp.com/room/5ecd811acc547673cb887dc5',
        # 'https://www.dabangapp.com/room/5ec8a34e1e5a900bc9397fa4',
        # 'https://www.dabangapp.com/room/5ed5fd6363f8bd3a2303ad00',
        # 'https://www.dabangapp.com/room/5ee1ca842da3e67031980e10',
        # 'https://www.dabangapp.com/room/5ee1a6023a529c286169def6',
        # 'https://www.dabangapp.com/room/5ecccf980af94861809bbc80',
        # 'https://www.dabangapp.com/room/5ed9c99251070c6a71e9536f',
        # 'https://www.dabangapp.com/room/5eddcee2db31592a82696f72',
        # 'https://www.dabangapp.com/room/5ed44f01fd8b5310d016518e',
        # 'https://www.dabangapp.com/room/5ee1933526e2a52c944c7b17',
        # 'https://www.dabangapp.com/room/5eda0621d2e9b83ad8cceb6c',
        # 'https://www.dabangapp.com/room/5ecd811b5665d273cb6fbc2a',
        # 'https://www.dabangapp.com/room/5ee1d3449c95b4291f1e198f',
        # 'https://www.dabangapp.com/room/5ee2d7f4236bca61353c456f',
        # 'https://www.dabangapp.com/room/5ee20ca5d502e5178d34c3f2',
        # 'https://www.dabangapp.com/room/5ee20cadf980de178d1ed7e9',
        # 'https://www.dabangapp.com/room/5ed5b0744dfe7f567ca768d4',
        # 'https://www.dabangapp.com/room/5ee1a97f49af0b62de2ffe0d',
        # 'https://www.dabangapp.com/room/5ed9e4655c1f9078af86ffa2',
        # 'https://www.dabangapp.com/room/5ed453a8da937762d2858ed0',
        # 'https://www.dabangapp.com/room/5ede0c52fe9b5d410e2535d2',
        # 'https://www.dabangapp.com/room/5ee056a36aaf300f8fa42f27',
        # 'https://www.dabangapp.com/room/5eddecb4bb1ae12fc3dd0659',
        # 'https://www.dabangapp.com/room/5ed47ac4fcee5d5fee61ee69',
        # 'https://www.dabangapp.com/room/5ede17d3603496276fedb2a8',
        # 'https://www.dabangapp.com/room/5ecdc2ff8ef42b4fd64e0d54',
        # 'https://www.dabangapp.com/room/5ecf52cbb32831248a20ea34',
        # 'https://www.dabangapp.com/room/5ee20a547f236370256fb5e3',
        # 'https://www.dabangapp.com/room/5edf26370828337877d7d318',
        # 'https://www.dabangapp.com/room/5ed451b9aa3d4b3f04f7a8dd',
        # 'https://www.dabangapp.com/room/5ecf14ab91572e7b90ef3925',
        # 'https://www.dabangapp.com/room/5ee19ba2d5fd38489c355eb3',
        # 'https://www.dabangapp.com/room/5ecf7a060a46db6b7d406768',
        # 'https://www.dabangapp.com/room/5ee04986bbc720751f7015d5',
        # 'https://www.dabangapp.com/room/5ed60d50db899a053eda3775',
        # 'https://www.dabangapp.com/room/5ecf64a8c6cd48224af21baf',
        # 'https://www.dabangapp.com/room/5edaf725d0c9a3278047c0ed',
        # 'https://www.dabangapp.com/room/5ee036c7cd9a3978afd42a6c',
        # 'https://www.dabangapp.com/room/5ee2f24f364e4d68d156d772',
        # 'https://www.dabangapp.com/room/5eda064c547c253ad8aedfc6',
        # 'https://www.dabangapp.com/room/5ee08824bcf32b5e10795589',
        # 'https://www.dabangapp.com/room/5ec8f43e794cfd23fee732b7',
        # 'https://www.dabangapp.com/room/5ed5a1cc50881836ae72f8db',
        # 'https://www.dabangapp.com/room/5ee056a3fa1e760f8f9c2d5c',
        # 'https://www.dabangapp.com/room/5ece43e1f6ccb22d1d1631d6',
        # 'https://www.dabangapp.com/room/5edd9acdd8758b0f2f9a68c7',
        # 'https://www.dabangapp.com/room/5ec606659015282ec13d1d09',
        # 'https://www.dabangapp.com/room/5ed077912de6947024a8adde',
        # 'https://www.dabangapp.com/room/5ee32f4c68c9422597a74be1',
        # 'https://www.dabangapp.com/room/5ed9c627958f9314cba5c8b3',
        # 'https://www.dabangapp.com/room/5ec8b5f71779b373868479a7',
        # 'https://www.dabangapp.com/room/5edf10cf0432e14c1361c3bf',
        # 'https://www.dabangapp.com/room/5ec8f44195691a23fe88850f',
        # 'https://www.dabangapp.com/room/5edd9698fae56c1d5c7ce734',
        # 'https://www.dabangapp.com/room/5ee1d87d846234043f7dffa7',
        # 'https://www.dabangapp.com/room/5eddbc430fcea544a68060e0',
        # 'https://www.dabangapp.com/room/5ed4514bf799ad2e7c231795',
        # 'https://www.dabangapp.com/room/5ee2d7e17ecfe561352dbefc',
        # 'https://www.dabangapp.com/room/5ec1f2e21efa397d1a4674a0',
        # 'https://www.dabangapp.com/room/5ed4538aac6f6a62d25e28ec',
        # 'https://www.dabangapp.com/room/5ede375c2a1a570819223525',
        # 'https://www.dabangapp.com/room/5ee1a602e4af8c2861c2f19a',
        # 'https://www.dabangapp.com/room/5ee3030b97e5025424c9615f',
        # 'https://www.dabangapp.com/room/5ee480f4f0420a364e5eb77d',
        # 'https://www.dabangapp.com/room/5ed7544a1aa1c42cdc892e1f',
        # 'https://www.dabangapp.com/room/5ed0922cc2427005ddd3d108',
        # 'https://www.dabangapp.com/room/5edf3ba86fe6b44c28d14840',
        # 'https://www.dabangapp.com/room/5ec7a9d34c231c1de8fa2c59',
        # 'https://www.dabangapp.com/room/5ecf66ac810cd13efaf7527a',
        # 'https://www.dabangapp.com/room/5ee4249f95cdae7d4ff40ce8',
        # 'https://www.dabangapp.com/room/5ededdd8c90ccc473e379d6d',
        # 'https://www.dabangapp.com/room/5ec7a9d73a3d591de867a1ae',
        # 'https://www.dabangapp.com/room/5ed4537a16aa3862d26524bd',
        # 'https://www.dabangapp.com/room/5ed6073af5b40f0ddcb7db00',
        # 'https://www.dabangapp.com/room/5ed453c6cb3a8e62d25f3e22',
        # 'https://www.dabangapp.com/room/5ed4a0dc8b96645d4bcefe45',
        # 'https://www.dabangapp.com/room/5ed88be87a17ff4c109202a0',
        # 'https://www.dabangapp.com/room/5ec8f43eeb60c823fed6d426',
        # 'https://www.dabangapp.com/room/5ed87a0b3fe70040efab351f',
        # 'https://www.dabangapp.com/room/5ee0820baa6fcf59f86f4017',
        # 'https://www.dabangapp.com/room/5ee18956cc9d714ff9e90a58',
        # 'https://www.dabangapp.com/room/5ee060d9ee83244996c7405b',
        # 'https://www.dabangapp.com/room/5ec7a77b648c6b1740ab1f62',
        # 'https://www.dabangapp.com/room/5edda32600467e2788c15346',
        # 'https://www.dabangapp.com/room/5ee3427a6c90a24c29c11e7a',
        # 'https://www.dabangapp.com/room/5ed7535a5cd62d6e038033c3',
        # 'https://www.dabangapp.com/room/5ed5eda8b0cde824174bc25d',
        # 'https://www.dabangapp.com/room/5ec1e90cc35a9d1ccd748766',
        # 'https://www.dabangapp.com/room/5ed0bb6d692c263a8bb25e91',
        # 'https://www.dabangapp.com/room/5ed5cfab1c918f174a0f2325',
        # 'https://www.dabangapp.com/room/5edd8b9a4b03b85122cd9175',
        # 'https://www.dabangapp.com/room/5ed217d134d1710accd4f003',
        # 'https://www.dabangapp.com/room/5ed6f4c9cd868b073335e544',
        # 'https://www.dabangapp.com/room/5ede0acae3c9ed35334cb536',
        # 'https://www.dabangapp.com/room/5eddd364f6e080194f21187b',
        # 'https://www.dabangapp.com/room/5ec60d0bb3d4462ce81c6db2',
        # 'https://www.dabangapp.com/room/5ecb0ed0c692bc5e8bfe2daf',
        # 'https://www.dabangapp.com/room/5ed5cf7d3ecb65174ab55b7b',
        # 'https://www.dabangapp.com/room/5edd8b6c7f39365122ae9f21',
        # 'https://www.dabangapp.com/room/5ed61f9735802a02fe7297e4',
        # 'https://www.dabangapp.com/room/5ede14c437d17f67bd43cb81',
        # 'https://www.dabangapp.com/room/5ed461025f6504189da0dab3',
        # 'https://www.dabangapp.com/room/5ec621694675f14e751cb103',
        # 'https://www.dabangapp.com/room/5ecc7546fef930225137e619',
        # 'https://www.dabangapp.com/room/5ed1d1b5b0841d09eb423a85',
        # 'https://www.dabangapp.com/room/5ec20192afffb02315b07055',
        # 'https://www.dabangapp.com/room/5ed46322a79f5d416eea715b',
        # 'https://www.dabangapp.com/room/5ed474b1c06a4650d64f195a',
        # 'https://www.dabangapp.com/room/5ed05ad205d0de105dc7ea07',
        # 'https://www.dabangapp.com/room/5ed5cf407b3999174a020a31',
        # 'https://www.dabangapp.com/room/5ecb5fd82709fc53c1ef8523',
        'https://www.dabangapp.com/room/5ed605132730206424b3ad23',
        'https://www.dabangapp.com/room/5edef1775129df67c15c83aa',
        'https://www.dabangapp.com/room/5edef1a8def92267c1278eb1',
        'https://www.dabangapp.com/room/5ed0921530dab905dde24d1f',
        'https://www.dabangapp.com/room/5ee2da29d5b7637e4ef88262',
        'https://www.dabangapp.com/room/5ee050cae52eac01a93c924d',
        'https://www.dabangapp.com/room/5ec32bac8e679c3874312ffa',
        'https://www.dabangapp.com/room/5ede36f48961957ebfbf0e24',
        'https://www.dabangapp.com/room/5ec1f1882490e94fa94e5c50',
        'https://www.dabangapp.com/room/5ed461438b6e072c88f4b872',
        'https://www.dabangapp.com/room/5ee040177584802d0206ecd9',
        'https://www.dabangapp.com/room/5ee33327690e022078d6d4b5',
        'https://www.dabangapp.com/room/5ee1ea615bd6a102a6f1ed8d',
        'https://www.dabangapp.com/room/5edf09913857c840ff57a4b5',
        'https://www.dabangapp.com/room/5edd96adbf25b01d5c78ef8d',
        'https://www.dabangapp.com/room/5ec343809181002b5a70cd90',
        'https://www.dabangapp.com/room/5ee04af10d7ba90e12f9372f',
        'https://www.dabangapp.com/room/5ed8b2481e7ae343c0d84f79',
        'https://www.dabangapp.com/room/5ed46e5c76471648af7a3c92',
        'https://www.dabangapp.com/room/5ee435d2c1c5017b65467b68',
        'https://www.dabangapp.com/room/5ed5fc0d66f5a83087f70871',
        'https://www.dabangapp.com/room/5edf3e809ae5e702a0353bf9',

        # 오피스텔

        'https://www.dabangapp.com/room/5ee31af149799f74b39697b9',
        'https://www.dabangapp.com/room/5ea0f58193c1372ac2df539f',
        'https://www.dabangapp.com/room/5ed75f2940907a6275f81119',
        'https://www.dabangapp.com/room/5ed5aeff393bf47b34a023b6',
        'https://www.dabangapp.com/room/5ee1cff049937b0cd5a4768c',
        'https://www.dabangapp.com/room/5ecb7b6f5f8c86337c2d82ee',
        'https://www.dabangapp.com/room/5ec76ca5fd5b34061cda84ab',
        'https://www.dabangapp.com/room/5ec49e8e1a664b60c3898a5a',
        'https://www.dabangapp.com/room/5eba122609dbf925dd697447',
        'https://www.dabangapp.com/room/5ec1ed01f4f6e96a2eff1088',
        'https://www.dabangapp.com/room/5ee474320a87ed35b6e1f148',
        'https://www.dabangapp.com/room/5ee1d00eea44c70cd5974104',
        'https://www.dabangapp.com/room/5edd8bbc4da0767c63321a2f',
        'https://www.dabangapp.com/room/5ee2d8d533527a0c95846185',
        'https://www.dabangapp.com/room/5ed5ab45eab3c46e515e3663',
        'https://www.dabangapp.com/room/5ee3145316cccc6c8cc81be2',
        'https://www.dabangapp.com/room/5ed496d8e7e30064ad7408a5',
        'https://www.dabangapp.com/room/5ec8e7fca7f97320ca8bbf0c',
        'https://www.dabangapp.com/room/5ed848cd1e8e392a54d8551d',
        'https://www.dabangapp.com/room/5ed88c1bc1d6602c3d9f64e0',
        'https://www.dabangapp.com/room/5ee480b834013643886f1e56',
        'https://www.dabangapp.com/room/5eb815542a5f504a1269c63b',
        'https://www.dabangapp.com/room/5ee1e967c094aa1e793673df',
        'https://www.dabangapp.com/room/5ea934f7cb0ad47994b296df',
        'https://www.dabangapp.com/room/5b0e2eea5ed74c7355786247',
        'https://www.dabangapp.com/room/5edddf7387e0a470abfd3ac9',
        'https://www.dabangapp.com/room/5ec36c774a220d7e916e56d1',
        'https://www.dabangapp.com/room/5ee1937fbaba7c2e5a455904',
        'https://www.dabangapp.com/room/5ed4dfaa5f170073ee8d7fcd',
        'https://www.dabangapp.com/room/5ee4bf95dbf00f30cc24c3b6',
        'https://www.dabangapp.com/room/5eb4f74c05d0994834879de3',
        'https://www.dabangapp.com/room/5ed07091c030fa3d8b494af2',
        'https://www.dabangapp.com/room/5ecb438deac8290cd9533e16',
        'https://www.dabangapp.com/room/5edafc9aeb474d119f0f5697',
        'https://www.dabangapp.com/room/5ea65cb7aa04a31d3ce76eb4',
        'https://www.dabangapp.com/room/5ed4907d1be743473b69cade',
        'https://www.dabangapp.com/room/5ed1b13015d21122088c1a05',
        'https://www.dabangapp.com/room/5ecb7b78f03815584553d447',
        'https://www.dabangapp.com/room/5ee480a93093e44dbce4ab07',
        'https://www.dabangapp.com/room/5ecc69808e45ce74469dc38a',
        'https://www.dabangapp.com/room/5ee2d8c4c536760c93a0bf53',
        'https://www.dabangapp.com/room/5ebf7fdbe83bfb38a2adead6',
        'https://www.dabangapp.com/room/5ee4961531171e1f3308b2fd',
        'https://www.dabangapp.com/room/5ed6723f6862332078fb38be',
        'https://www.dabangapp.com/room/5c7ce8e4fdfd1851bd92a57e',
        'https://www.dabangapp.com/room/5edcfe6847a649051d135d57',
        'https://www.dabangapp.com/room/5e33bb027bfab713de85a774',
        'https://www.dabangapp.com/room/5ed88c229204952c3d297bc0',
        'https://www.dabangapp.com/room/5ed4d7c41de6ad6b4dc961e2',
        'https://www.dabangapp.com/room/5ed76633f99e8a214586160c',
        'https://www.dabangapp.com/room/5e0f3718d96bea310291e09a',
        'https://www.dabangapp.com/room/5ed88c14107ba22083b69095',
        'https://www.dabangapp.com/room/5ed48ab6fc276065066e8dd8',
        'https://www.dabangapp.com/room/5ebdf1bd9d74a430467f69db',
        'https://www.dabangapp.com/room/5ee42fa8664d0453d1dc13dd',
        'https://www.dabangapp.com/room/5ecb83382305bf1403795dcf',
        'https://www.dabangapp.com/room/5ed3199f604fca14ae17294a',
        'https://www.dabangapp.com/room/5ed6f947682c9f23dd3229e4',
        'https://www.dabangapp.com/room/5ece134ece8b89563b932576',
        'https://www.dabangapp.com/room/5ec772565cc5400d6c0cee63',
        'https://www.dabangapp.com/room/5eda5cc75b7ed9227c5e3f67',
        'https://www.dabangapp.com/room/5ecfa595388def306ee34d27',
        'https://www.dabangapp.com/room/5ed75e4e5c06cb737beba206',
        'https://www.dabangapp.com/room/5ee4429cf38d136de04d38cd',
        'https://www.dabangapp.com/room/5ed07099c5d9472dc7ab36dd',
        'https://www.dabangapp.com/room/5e9960100d9b5158f03c1317',
        'https://www.dabangapp.com/room/5ec61380f03a461377144d3e',
        'https://www.dabangapp.com/room/5e19204fd1e8ba59c8b5d7f4',
        'https://www.dabangapp.com/room/5edc4acdc0824757640c4a3d',
        'https://www.dabangapp.com/room/5ed319a5f3ba232524040ff4',
        'https://www.dabangapp.com/room/5e93d057bc9e1620963edf68',
        'https://www.dabangapp.com/room/5ec56a7ed1de534f3331427f',
        'https://www.dabangapp.com/room/5ec8c64bedf29f0b2830d6c8',
        'https://www.dabangapp.com/room/5ec7a6cf41b0ec5bf6603411',
        'https://www.dabangapp.com/room/5d89b7deb3be6628c11e79d4',
        'https://www.dabangapp.com/room/5ec4e238641ca66d6583d18a',
        'https://www.dabangapp.com/room/5ed9d92ec040f211cea551e5',
        'https://www.dabangapp.com/room/5ec8e01e44f9941a8096e199',
        'https://www.dabangapp.com/room/5edfdf0ca672d94e103f4f3c',
        'https://www.dabangapp.com/room/5ec4c9ca866921484b7a03bb',
        'https://www.dabangapp.com/room/5ed5ab5f8e2e730c14324fe3',
        'https://www.dabangapp.com/room/5ec8e0b422caac200e4d6589',
        'https://www.dabangapp.com/room/5eb2089fd0b54f35941dc742',
        'https://www.dabangapp.com/room/5e8d36c5643ef26fe5d7a23a',
        'https://www.dabangapp.com/room/5ee3082188618e529e576be9',
        'https://www.dabangapp.com/room/5ebfe21c6e081f26bd9d6718',
        'https://www.dabangapp.com/room/5c8319179435f455bfadb906',
        'https://www.dabangapp.com/room/5e91566b0f96861e75b1b60f',
        'https://www.dabangapp.com/room/5ed5a6ef2226205b78b797f8',
        'https://www.dabangapp.com/room/5ee2f4f4ae651d6bbd92e7c9',
        'https://www.dabangapp.com/room/5ed4c2db58b05059f1dd0d4a',
        'https://www.dabangapp.com/room/5ee1cf45a3384867bd23762c',
        'https://www.dabangapp.com/room/5eafe092fe13e337eebd331c',
        'https://www.dabangapp.com/room/5ecc9d1a1b54bf738058a35b',
        'https://www.dabangapp.com/room/5ec720687e089d32a60d508f',
        'https://www.dabangapp.com/room/5ec8df3193704c1c48507d54',
        'https://www.dabangapp.com/room/5ebcdf04e697ac58e89e6f73'

    ]
    # 각 게시글 조회 시작
    for post_index, dabang_url in enumerate(url_all_list):
        print('############################################# 다음 url \n')
        print('url 입니다.', dabang_url, '\n')
        driver.get(dabang_url)
        time.sleep(2)

        post_type = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/p/span')
        post_type = post_type.get_attribute('innerText')

        # 상세 더보기 클릭
        try:
            button = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div/button')
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            pass
        # 방 정보 설명
        description = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div/div")
        description = description[0].get_attribute("innerText")
        description = description.replace("\n", "")

        try:
            if '접기' in description:
                description = description.split('접기')
                description = description[0]

        except IndexError:
            pass

        # 매물 형식
        unrefined_salesform = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/div')
        salesForm = unrefined_salesform[0].get_attribute("innerText")
        salesForm = salesForm.replace('/', ' ')
        salesForm = salesForm.replace('\n', '')
        salesForm = salesForm.split()
        salesType = salesForm[0]  # sales type

        print(salesType)
        print(post_type)
        if salesType == '매매':

            try:
                btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[3]/button')
                driver.execute_script("arguments[0].click();", btn)

                href = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/a')
                href = href.get_attribute('href')
                print(href)
                driver.get(href)
                time.sleep(1)
                # 중개소 정보 더 보기
                companyName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[1]/div')
                print(companyName)
                companyName = companyName.get_attribute('innerText')
                print(companyName)

                address = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[8]/div')
                address = address.get_attribute('innerText')
                print(address)
                managerName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[2]/div')
                managerName = managerName.get_attribute('innerText')
                print(managerName)
                tel = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[3]/div')
                tel = tel.get_attribute('innerText')
                print(tel)
                companyNumber = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[4]/div')
                companyNumber = companyNumber.get_attribute('innerText')
                print(companyNumber)
                brokerage = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[5]/div')
                brokerage = brokerage.get_attribute('innerText')
                print(brokerage)
                dabangCreated_at = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[6]/div')
                dabangCreated_at = dabangCreated_at.get_attribute('innerText')
                print(dabangCreated_at)
                successCount = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[7]/div')
                successCount = successCount.get_attribute('innerText')
                print(successCount)
                image = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div')
                image = image.get_attribute('class')
                image = image.split(' ')
                image = image[1]
                print(image)
                photo = driver.execute_script(
                    f'return window.getComputedStyle(document.querySelector(".{image}"),":after").getPropertyValue("background")')
                print(photo)
                test_url = re.findall(r'"(.*?)"', photo)
                test_url = test_url[0]
                print(test_url)

            except NoSuchElementException:
                managerName = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[1]')
                managerName = managerName.get_attribute('innerText')
                if '(' in managerName:
                    managerName = managerName.split('(')
                    managerName = managerName[0]
                tel = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[2]')
                tel = tel.get_attribute('innerText')
                if '-' in tel:
                    tel = tel.replace('-', '')
                companyName = None
                address = None
                test_url = None
                companyNumber = None
                brokerage = None
                dabangCreated_at = None
                successCount = None


        else:

            try:
                btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[4]/button')
                driver.execute_script("arguments[0].click();", btn)

                href = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/a')
                href = href.get_attribute('href')
                print(href)
                driver.get(href)
                time.sleep(1)
                # 중개소 정보 더 보기
                companyName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[1]/div')
                print(companyName)
                companyName = companyName.get_attribute('innerText')
                print(companyName)

                address = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[8]/div')
                address = address.get_attribute('innerText')
                print(address)
                managerName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[2]/div')
                managerName = managerName.get_attribute('innerText')
                print(managerName)
                tel = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[3]/div')
                tel = tel.get_attribute('innerText')
                print(tel)
                companyNumber = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[4]/div')
                companyNumber = companyNumber.get_attribute('innerText')
                print(companyNumber)
                brokerage = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[5]/div')
                brokerage = brokerage.get_attribute('innerText')
                print(brokerage)
                dabangCreated_at = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[6]/div')
                dabangCreated_at = dabangCreated_at.get_attribute('innerText')
                print(dabangCreated_at)
                successCount = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[7]/div')
                successCount = successCount.get_attribute('innerText')
                print(successCount)
                image = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div')
                image = image.get_attribute('class')
                image = image.split(' ')
                image = image[1]
                print(image)
                photo = driver.execute_script(
                    f'return window.getComputedStyle(document.querySelector(".{image}"),":after").getPropertyValue("background")')
                print(photo)
                test_url = re.findall(r'"(.*?)"', photo)
                test_url = test_url[0]
                print(test_url)

            except NoSuchElementException:
                managerName = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[1]')
                managerName = managerName.get_attribute('innerText')
                if '(' in managerName:
                    managerName = managerName.split('(')
                    managerName = managerName[0]
                tel = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[2]')
                tel = tel.get_attribute('innerText')
                if '-' in tel:
                    tel = tel.replace('-', '')
                companyName = None
                address = None
                test_url = None
                companyNumber = None
                brokerage = None
                dabangCreated_at = None
                successCount = None
        # button = driver.find_element_by_xpath("/html/body/div[4]/div/div/header/button")
        # driver.execute_script("arguments[0].click();", button)

        broker_ins = Broker.objects.get_or_create(
            companyName=companyName,
            address=address,
            managerName=managerName,
            tel=tel,
            image=test_url,
            companyNumber=companyNumber,
            brokerage=brokerage,
            dabangCreated_at=dabangCreated_at,
            successCount=successCount,
        )
        print(broker_ins)
        # 상세 설명 보기
        driver.get(dabang_url)
        print('--')
        try:
            button = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/button")
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            pass

        # 매물 형태
        time.sleep(2)
        print('--')
        salesDepositChar = salesForm[1]
        if salesDepositChar.find('원'):
            salesDepositChar = salesDepositChar.replace('원', '')

        salesdepositInt = salesDepositChar.replace('억', '00000000')
        if salesdepositInt.find('만'):
            salesdepositInt = salesdepositInt.replace('만', '')
        salesdepositInt = int(salesdepositInt)

        try:
            salesmonthlyChar = salesForm[2]

            salesmonthlyInt = salesmonthlyChar.replace('만원', '')
            salesmonthlyInt = int(salesmonthlyInt)

            if salesType == '전세':
                # 전세는 금액이 억, 만원이 붙어 있는 경우가 있어서 이렇게 처리.
                salesdepositInt = salesdepositInt + salesmonthlyInt
                salesDepositChar = salesDepositChar + salesmonthlyChar
        except IndexError:
            salesmonthlyInt = 0
            salesmonthlyChar = ''

        salesform_ins = SalesForm.objects.create(
            type=salesType,
            depositChar=salesDepositChar,
            monthlyChar=salesmonthlyChar,
            depositInt=salesdepositInt,
            monthlyInt=salesmonthlyInt,
        )

        if post_type == "아파트":
            if salesType == "매매":
                address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/p')
            else:
                address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/p')
        else:
            address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[4]/div/p')
        if not address:
            address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div/div/p')

        try:
            address = address[0].get_attribute('innerText')
            if '※' in address:
                address = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[4]/div/p')

                address = address.get_attribute('innerText')
            print('address >>>>>>>>>>>>', address)
        except NoSuchElementException:
            address = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/p')
            address = address.get_attribute('innerText')

        # kakao Local API
        url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
        res = requests.get(url, headers={'Authorization': f'KakaoAK {KAKAO_APP_ID}'})
        str_data = res.text
        json_data = json.loads(str_data)
        lat = json_data['documents'][0]['x']
        lng = json_data['documents'][0]['y']
        print(f'lat, lng >>  {lat} {lng}')
        address_ins, __ = PostAddress.objects.get_or_create(
            loadAddress=address,
        )
        print('address_ins', address_ins)

        unrefined_floor = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[1]/div')
        total_floor = unrefined_floor[0].get_attribute('innerText')
        total_floor = total_floor.split('/')
        floor = total_floor[0]

        totalFloor = total_floor[1]
        totalFloor = totalFloor.replace(' ', '')

        areaChar = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
        areaChar = areaChar[0].get_attribute('innerText')

        # 평수로 변환하는 버
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/button').click()

        unrefined_area = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
        supplyAreaChar = unrefined_area[0].get_attribute('innerText')

        supplyAreaInt = supplyAreaChar.split('/')
        supplyAreaInt = supplyAreaInt[1].replace('평', '')

        supplyAreaInt = supplyAreaInt.strip()

        supplyAreaInt = int(supplyAreaInt)

        if post_type == '아파트':
            if salesType == '매매':
                shortRent = False
            else:
                shortRent = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[5]/p')
                shortRent = shortRent[0].get_attribute('innerText')
        else:
            if salesType == '매매':
                shortRent = False
            else:
                shortRent = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[5]/p')
                if not shortRent:
                    shortRent = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                shortRent = shortRent[0].get_attribute('innerText')
        print('shortRent is >>', shortRent)

        if shortRent == '불가능':
            shortRent = False
        else:
            shortRent = True

        # 관리비 클래스
        try:
            if post_type == "아파트":
                management = driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]')
            else:
                if salesType == "매매":
                    management = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[2]')
                else:
                    management = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]')
        except NoSuchElementException:
            management = None

        try:
            management = management.get_attribute('innerText')
            management = management.replace('\n', '')
            management = management.replace(' ', '')
            management = management.replace('(', ' ')
            management = management.replace(')', ' ')
            management = management.replace(',', ' ')
            management = management.strip(' ')
            management = management.split(' ')

        except AttributeError:
            pass

        try:
            managementPay = management.pop(0)
            if managementPay.find('만원'):
                managementPay = managementPay.replace('만원', ' ')
                if managementPay == '없음':
                    managementPay = 0
                elif managementPay == '문의':
                    managementPay = 0
                managementPay = float(managementPay)
            else:
                managementPay = 0
            totalFee = managementPay

        except IndexError:
            pass
        except AttributeError:
            pass
        except NameError:
            pass

        # 관리비 마무리

        parkingPay = None
        # 주차비 관련
        try:
            if post_type == "아파트":
                if salesType == "매매":
                    parkingDetail = '가능(무료)'
                    parkingTF = True
                else:
                    parkingDetail = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                    parkingDetail = parkingDetail.get_attribute('innerText')
            else:
                if salesType == "매매":
                    try:
                        parkingDetail = driver.find_element_by_xpath(
                            "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]")
                    except NoSuchElementException:
                        parkingDetail = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
                    except IndexError:
                        parkingDetail = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
                    parkingDetail = parkingDetail.get_attribute('innerText')

                else:
                    try:
                        parkingDetail = driver.find_element_by_xpath(
                            "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[4]/p")
                        parkingDetail = parkingDetail.get_attribute('innerText')
                    except NoSuchElementException:
                        parkingDetail = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                        parkingDetail = parkingDetail.get_attribute('innerText')

        except IndexError:
            unrefined_parking = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p'
            )
            parkingDetail = unrefined_parking[0].get_attribute('innerText')

        except TypeError:
            parkingDetail = '불가'
        if '만' in parkingDetail:
            parkingDetail = parkingDetail.split('만')
            parkingDetail = parkingDetail[0]
            parkingPay = float(parkingDetail)
            parkingDetail = '문의'

        # parking Tf
        if parkingDetail == '가능(무료)':
            parkingTF = True
        elif parkingDetail == '문의':
            parkingTF = True
        else:
            parkingTF = False
        print('parking >>>>>>>>>>>>>', parkingDetail, parkingTF, parkingPay)
        try:
            if not salesType == "매매":
                if post_type == "아파트":
                    unrefined_living_expenses = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/div/div/label')
                    unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/div/div/span')
                else:
                    try:
                        unrefined_living_expenses = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[2]/div/div/div/label')
                        unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[2]/div/div/div/span')
                    except NoSuchElementException:
                        unrefined_living_expenses = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/div/div/label')
                        unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p[2]/span')
            else:
                living_expenses = None
                living_expenses_detail = None
        except NoSuchElementException:
            pass

        # 생활비 , 생활비 항목들
        try:
            unrefined_living_expenses = unrefined_living_expenses[0].get_attribute('innerText')
            living_expenses = unrefined_living_expenses.replace(' ', '')
            living_expenses_detail = unrefined_living_expenses_detail[0].get_attribute('innerText')

        except IndexError:
            unrefined_living_expenses = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/div/div/label'
            )
            unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/div/div/span')
            unrefined_living_expenses = unrefined_living_expenses[0].get_attribute('innerText')
            living_expenses = unrefined_living_expenses.replace(' ', '')
            living_expenses_detail = unrefined_living_expenses_detail[0].get_attribute('innerText')
        except TypeError:
            print('생활비 항목 타입 에러')
        except NameError:
            print('생활비 항목 이름 에러')
        except AttributeError:
            print(unrefined_living_expenses, "가 없")

        if salesType == "매매":
            if post_type == "아파트":
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
            else:
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
        else:
            if post_type == "아파트":
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')
            else:
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')

        moveInChar = moveInChar.get_attribute('innerText')
        moveInDate = None
        if '날짜' in moveInChar:
            pass
        elif '즉시' in moveInChar:
            pass
        elif '2' in moveInChar:
            moveInChar = moveInChar.replace('.', '-')
            moveInDate = moveInChar
            moveInChar = '날짜 협의'
        else:
            moveInChar = '날짜 협의'

        print(moveInChar)

        # option & sceurity
        try:
            option_tag = driver.find_element_by_name('option')
            option_tag = option_tag.get_attribute('innerText')
            option_tag = option_tag.split('보안/안전시설')
            print('option tag >> ', option_tag)
            option = option_tag[0]
            option = option.split('\n\n')
            print(option)
            del option[0]
            del option[-1]
            print(option)

            print('result option', option)

            security = option_tag[1]
            security = security.split('\n\n')
            del security[-1]
            del security[0]
            print('result security', security)
        except IndexError:
            print('안전 시설 없음.')
            security = None
        except NoSuchElementException:
            print('옵션, 안전시설 없음', url)
            option = None
            security = None

        # Room option instance create
        if option is not None:
            option_list = []
            # POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/.option/')
            for option_name in option:
                # f = open(os.path.join(POSTS_IMAGE_DIR, f'{option_name}.png'), 'rb')
                ins = OptionItem.objects.get_or_create(
                    name=option_name,
                    # image=File(f),
                )
                # f.close()

                option_list.append(ins[0])

        # Security option instance create
        if security is not None:
            # POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/.security/')
            security_list = []
            print('안전 시설은 ', security)

            for security_name in security:
                # f = open(os.path.join(POSTS_IMAGE_DIR, f'{security_name}.png'), 'rb')
                ins = SecuritySafetyFacilities.objects.get_or_create(
                    name=security_name,
                    # image=File(f),
                )
                # f.close()

                security_list.append(ins[0])
                print('security >>>', ins[0])

        heatingType = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[3]/div')
        heatingType = heatingType.get_attribute('innerText')

        if salesType == "매매":
            if post_type == "아파트":
                pet = True
            else:
                pet = True
        else:
            if post_type == "아파트":
                pet = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
            else:
                pet = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            pet = pet.get_attribute('innerText')
            if pet == "불가능":
                pet = False
            else:
                pet = True

        if post_type == "아파트":
            elevator = True
        else:
            elevator = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[5]/div')
            elevator = elevator.get_attribute('innerText')
            if elevator == "있음":
                elevator = True
            else:
                elevator = False

        if post_type == "아파트":
            builtIn = True
        else:
            builtIn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[4]/div')
            builtIn = builtIn.get_attribute('innerText')
            if builtIn == "아님":
                builtIn = False
            else:
                builtIn = True
        # 베란다
        if post_type == "아파트":
            veranda = True
        else:
            if salesType == '매매':
                veranda = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
                veranda = veranda.get_attribute('innerText')
                if veranda == "있음":
                    veranda = True
                else:
                    veranda = False
            else:
                veranda = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
                veranda = veranda.get_attribute('innerText')
                if veranda == '있음':
                    veranda = True
                else:
                    veranda = False
        # depositLoan 전세 대출 자금
        if post_type == '아파트':
            if salesType == '매매':
                depositLoan = True
            else:
                depositLoan = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[8]/div')
                depositLoan = depositLoan.get_attribute('innerText')
                if depositLoan == '가능':
                    depositLoan = True
                else:
                    depositLoan = False
        else:
            if salesType == '매매':
                depositLoan = True
            else:
                depositLoan = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[8]/div')
                depositLoan = depositLoan.get_attribute('innerText')
                if depositLoan == '가능':
                    depositLoan = True
                else:
                    depositLoan = False

        # totalCitizen
        if post_type == '아파트':
            totalCitizen = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[5]/div')
            totalCitizen = totalCitizen.get_attribute('innerText')
        else:
            totalCitizen = None

        if post_type == "아파트":
            totalPark = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            totalPark = totalPark.get_attribute('innerText')
        else:
            totalPark = None

        if post_type == "아파트":
            totalPark = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            totalPark = totalPark.get_attribute('innerText')
        else:
            totalPark = None

        # 준공 완료일
        if post_type == '아파트':
            complete = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[4]/div')
            complete = complete.get_attribute('innerText')
        else:
            complete = None

        # 아파트 단지정보 크롤링 시작
        if post_type == '아파트':
            complex_detail_url = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[2]/div/a')
            complex_detail_url = complex_detail_url.get_attribute('href')
            driver.get(complex_detail_url)
            time.sleep(2)
            apart_name = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/h1')
            apart_name = apart_name.get_attribute('innerText')
            print('apart_name', apart_name)

            made = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/p[2]')
            made = made.get_attribute('innerText')
            print('made', made)

            total_citizen = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[2]/p[2]')
            total_citizen = total_citizen.get_attribute('innerText')
            print('totalCitizen', total_citizen)

            personal_park = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[3]/p[2]')
            personal_park = personal_park.get_attribute('innerText')
            if ' ' in personal_park:
                personal_park = personal_park.split(' ')
                personal_park = personal_park[1]
            print('personal_park', personal_park)

            # 총 동 수
            total_number = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[4]/p[2]')
            total_number = total_number.get_attribute('innerText')
            print('total_number', total_number)

            heating_system = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[5]/p[2]')
            heating_system = heating_system.get_attribute('innerText')
            print('heating_system', heating_system)

            min_max_floor = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[6]/p[2]')
            min_max_floor = min_max_floor.get_attribute('innerText')
            print('minMaxFloor', min_max_floor)

            buildingType = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/table/tbody/tr[1]/td[1]')
            buildingType = buildingType.get_attribute('innerText')
            print('buildingType', buildingType)

            constructionCompany = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div/table/tbody/tr[1]/td[2]')
            constructionCompany = constructionCompany.get_attribute('innerText')
            print('constructionCompany', constructionCompany)

            fuel = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/table/tbody/tr[1]/td[4]')
            fuel = fuel.get_attribute('innerText')
            print('fuel', fuel)

            complex_type = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/table/tbody/tr[2]/td[1]')
            complex_type = complex_type.get_attribute('innerText')
            print('complex_type', complex_type)

            # 용적률
            floorAreaRatio = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/table/tbody/tr[2]/td[2]')
            floorAreaRatio = floorAreaRatio.get_attribute('innerText')
            print('floorAreaRatio', floorAreaRatio)

            # 건폐율
            dryWasteRate = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/table/tbody/tr[2]/td[3]')
            dryWasteRate = dryWasteRate.get_attribute('innerText')
            print('dryWasteRate', dryWasteRate)

            # 단지평당가 매매
            complexSale = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[1]/p[3]')
            complexSale = complexSale.get_attribute('innerText')
            print('complexSale', complexSale)

            # 단지평당가 전세
            complexPrice = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[1]/p[5]')
            complexPrice = complexPrice.get_attribute('innerText')
            print('complexPrice', complexPrice)

            areaSale = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[2]/p[3]')
            areaSale = areaSale.get_attribute('innerText')
            print('areaSale', areaSale)

            areaPrice = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[2]/p[5]')
            areaPrice = areaPrice.get_attribute('innerText')
            print('areaPrice', areaPrice)

            div_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div/div/div')

            complex_image_list = []

            for i, url in enumerate(div_list):
                try:
                    cls_name = url.get_attribute('class')
                    cls_name = cls_name.split(' ')
                    cls_name = cls_name[1]
                    photo = driver.execute_script(
                        f'return window.getComputedStyle(document.querySelector(".{cls_name}"),":after").getPropertyValue("background")')
                    recommend_image = re.findall(r'"(.*?)"', photo)
                    complex_image_list.append(recommend_image[0])
                except IndexError:
                    pass

            print('complex_image_list >>', complex_image_list)
            complex_obj, __ = ComplexInformation.objects.get_or_create(
                complexName=apart_name,
                buildDate=made,
                totalCitizen=total_citizen,
                personalPark=personal_park,
                totalNumber=total_number,
                heatingSystem=heating_system,
                minMaxFloor=min_max_floor,
                buildingType=buildingType,
                constructionCompany=constructionCompany,
                fuel=fuel,
                complexType=complex_type,
                floorAreaRatio=floorAreaRatio,
                dryWasteRate=dryWasteRate,
                complexSale=complexSale,
                complexPrice=complexPrice,
                areaSale=areaSale,
                areaPrice=areaPrice,
            )
            print(complex_obj)
            for index, image in enumerate(complex_image_list):
                try:
                    COMPLEX_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/complex{complex_obj.pk}/')
                    if not os.path.exists(COMPLEX_IMAGE_DIR):
                        os.makedirs(COMPLEX_IMAGE_DIR, exist_ok=True)

                    # 이미지 생성
                    image_save_name = os.path.join(COMPLEX_IMAGE_DIR, f'{index}.jpg')
                    urllib.request.urlretrieve(image, image_save_name)
                    f = open(os.path.join(COMPLEX_IMAGE_DIR, f'{index}.jpg'), 'rb')
                    ComplexImage.objects.get_or_create(
                        image=File(f),
                        complex=complex_obj,
                    )
                    while True:
                        complex_obj_len = len(complex_obj.compleximage_set.all())
                        if complex_obj_len >= 6:
                            complex_obj_relation_list = complex_obj.compleximage_set.all()
                            complex_obj_relation_list[0].delete()
                            print(f'{apart_name} 이미지 삭제')
                        else:
                            break
                    f.close()
                except FileExistsError:
                    print('이미 존재하는 파일')
            time.sleep(1)
            # 추천 단지 시작
            # 아파트 단지 이미지 div
            recommend_div_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/div/a/div')
            # 추천 단지 아파트 이름
            recommend_apat_name_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/div/a/p[1]')
            # 추천 단지 아파트
            recommend_apat_type_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/div/a/p[2]/span[1]')
            # 추천 단지 총 세대 수
            recommend_apat_total_citizen_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/div/a/p[2]/span[2]')
            # 추천 단지 설립일자 리스트
            recommend_apat_build_date_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/div/a/p[2]/span[3]')
            # 추천 단지 주소 리스트
            recommend_apat_address_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/div/a/p[3]')
            # 추천 단지 정보 링크 리스트
            recommend_apat_link_list = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[8]/div/ul/li/ul/li/a')

            for i, url in enumerate(recommend_div_list):
                cls_name = url.get_attribute('class')
                cls_name = cls_name.split(' ')
                cls_name = cls_name[1]

                photo = driver.execute_script(
                    f'return window.getComputedStyle(document.querySelector(".{cls_name}"),":before").getPropertyValue("background")')
                recommend_image_url = re.findall(r'"(.*?)"', photo)
                print('추천단지 이미지', recommend_image_url[0])
                recommend_apat_name = recommend_apat_name_list[i].get_attribute('innerText')
                print('추천단지 아파트 이름', recommend_apat_name)
                recommend_apat_type = recommend_apat_type_list[i].get_attribute('innerText')
                print('추천단지 아파트 타입', recommend_apat_type)
                recommend_apat_total_citizen = recommend_apat_total_citizen_list[i].get_attribute('innerText')
                print('추천 단지 총 세대 수', recommend_apat_total_citizen)
                recommend_apat_build_date = recommend_apat_build_date_list[i].get_attribute('innerText')
                print('추천 단지 설립 일자', recommend_apat_build_date)
                recommend_apat_address = recommend_apat_address_list[i].get_attribute('innerText')
                print('추천 단지 주소', recommend_apat_address)
                recommend_apat_link = recommend_apat_link_list[i].get_attribute('href')
                print('추천 단지 해당 링크', recommend_apat_link)

                # 이미지 생성
                try:
                    RECOMMEND_IMAGE_DIR = os.path.join(MEDIA_ROOT,
                                                       f'.posts/{apart_name}/')
                    if not os.path.exists(RECOMMEND_IMAGE_DIR):
                        os.makedirs(RECOMMEND_IMAGE_DIR, exist_ok=True)

                    # 이미지 생성
                    image_save_name = os.path.join(RECOMMEND_IMAGE_DIR, f'{recommend_apat_name}.jpg')
                    urllib.request.urlretrieve(recommend_image_url[0], image_save_name)
                    f = open(os.path.join(RECOMMEND_IMAGE_DIR, f'{recommend_apat_name}.jpg'), 'rb')
                    RecommendComplex.objects.get_or_create(
                        complex=complex_obj,
                        image=File(f),
                        name=recommend_apat_name,
                        type=recommend_apat_type,
                        totalCitizen=recommend_apat_total_citizen,
                        buildDate=recommend_apat_build_date,
                        address=recommend_apat_address,
                        link=recommend_apat_link,
                    )
                    f.close()

                except FileExistsError:
                    print('이미 존재하는 파일')
                #

                print('\n')
        else:
            complex_obj = None
            apart_name = None

        driver.get(dabang_url)
        time.sleep(1)
        # 아파트 단지 정보 종료.

        post = PostRoom.objects.get_or_create(
            broker=broker_ins[0],
            complex=complex_obj,
            type=post_type,
            name=apart_name,
            description=description,
            address=address_ins,
            salesForm=salesform_ins,
            lat=lng,
            lng=lat,
            floor=floor,
            totalFloor=totalFloor,
            areaChar=areaChar,
            supplyAreaChar=supplyAreaChar,
            supplyAreaInt=supplyAreaInt,
            shortRent=shortRent,
            parkingDetail=parkingDetail,
            parkingTF=parkingTF,
            parkingPay=parkingPay,
            living_expenses=living_expenses,
            living_expenses_detail=living_expenses_detail,
            moveInChar=moveInChar,
            moveInDate=moveInDate,
            heatingType=heatingType,
            pet=pet,
            elevator=elevator,
            builtIn=builtIn,
            veranda=veranda,
            depositLoan=depositLoan,
            totalCitizen=totalCitizen,
            totalPark=totalPark,
            complete=complete,
        )
        if management is not None:
            admin_instance_list = []
            for obj in management:
                admin_ins = AdministrativeDetail.objects.get_or_create(
                    name=obj,
                )
                admin_instance_list.append(admin_ins[0])
        else:
            admin_instance_list = None

        if admin_instance_list is not None:
            for ins in admin_instance_list:
                print('admin_instance_list : ins >>', ins)
                MaintenanceFee.objects.create(
                    postRoom=post[0],
                    totalFee=totalFee,
                    admin=ins,
                )

        if option is not None:
            for ins in option_list:
                RoomOption.objects.create(
                    postRoom=post[0],
                    option=ins,

                )
                print(ins)
        if security is not None:
            for ins in security_list:
                RoomSecurity.objects.create(
                    postRoom=post[0],
                    security=ins,

                )

        div_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div')

        image_list = []

        for i, url in enumerate(div_list):
            cls_name = url.get_attribute('class')
            cls_name = cls_name.split(' ')
            cls_name = cls_name[1]
            photo = driver.execute_script(
                f'return window.getComputedStyle(document.querySelector(".{cls_name}"),":after").getPropertyValue("background")')

            test_url = re.findall(r'"(.*?)"', photo)

            # 이미지 파일이 아닌 url를 뺀 새로운 url list
            if test_url:
                if 'dabang' in test_url[0]:
                    pass
                else:
                    image_list.append(test_url[0])
            else:
                print('빈 리스트')

        if image_list:
            for index, image_url in enumerate(image_list):
                print('image_url>> ', image_url)
                try:
                    POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/postroom{post[0].pk}/')
                    if not os.path.exists(POSTS_IMAGE_DIR):
                        os.makedirs(POSTS_IMAGE_DIR, exist_ok=True)

                    # 이미지 생성
                    image_save_name = os.path.join(POSTS_IMAGE_DIR, f'{index}.jpg')
                    urllib.request.urlretrieve(image_url, image_save_name)
                    f = open(os.path.join(POSTS_IMAGE_DIR, f'{index}.jpg'), 'rb')
                    PostImage.objects.get_or_create(
                        image=File(f),
                        post=post[0],
                    )
                    f.close()
                except FileExistsError:
                    print('이미 존재하는 파일')

        # print('이미지 업로드 끝')
        print('게시글 하나 크롤링 완성 pk:', post_index, '-========================================== \n ')

    driver.close()
