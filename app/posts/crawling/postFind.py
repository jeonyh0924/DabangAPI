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
        # 'https://www.dabangapp.com/room/5e992d31d9d3a15c88491696',
        # 'https://www.dabangapp.com/room/5e9e60010f85d2751c0ff977',
        # 'https://www.dabangapp.com/room/5e9efb251e60da5787550276',
        # 'https://www.dabangapp.com/room/5e992d30f30bdb6390449f94',
        # 'https://www.dabangapp.com/room/5eacf6b6de8f727055ff454c',
        # 'https://www.dabangapp.com/room/5e9fd1f1a639766eb587c9fc',
        # 'https://www.dabangapp.com/room/5ea68bcf4b33eb37381dd93d',
        # 'https://www.dabangapp.com/room/5e9001d9004a6b46f8e283bc',
        # 'https://www.dabangapp.com/room/5ea6658f73f5247e2527ee16',
        # 'https://www.dabangapp.com/room/5ea14be8a66c1345b3284e41',
        # 'https://www.dabangapp.com/room/5ea6660c65a9c97e26801afa',
        # 'https://www.dabangapp.com/room/5ea667d022bf735eb278c521',
        # 'https://www.dabangapp.com/room/5eafe0a2bb3158474215f0df',
        # 'https://www.dabangapp.com/room/5ea108010bc55f40bb3205d7',
        # 'https://www.dabangapp.com/room/5eafc9b12264457a00c76db4',
        # 'https://www.dabangapp.com/room/5eaf98f0332e0411c53486b0',
        # 'https://www.dabangapp.com/room/5ea8dad47f781b4a5d54e209',
        # 'https://www.dabangapp.com/room/5eafe0f99d4aca4742fcdb4f',
        # 'https://www.dabangapp.com/room/5ea792b860fdb47924f11ce6',
        # 'https://www.dabangapp.com/room/5eafd7dc64ed750d7dd19912',
        # 'https://www.dabangapp.com/room/5ea681128a6ab33164610bc3',
        # 'https://www.dabangapp.com/room/5eacee5d1b5b4a0571462a44',
        # 'https://www.dabangapp.com/room/5eafe15b121b79551aac9af4',
        # 'https://www.dabangapp.com/room/5ea7b6b42eeb9a577f75ef26',
        # 'https://www.dabangapp.com/room/5e901025f3ff9d77d2ee73f7',
        # 'https://www.dabangapp.com/room/5ea79470d8ff712a5255199e',
        # 'https://www.dabangapp.com/room/5e8d77eec22836604787ccb7',
        # 'https://www.dabangapp.com/room/5ead4ca08ac6793a10dc5d37',
        # 'https://www.dabangapp.com/room/5e9a8085ec0d5e2ef92ba4b0',
        # 'https://www.dabangapp.com/room/5e991254697bff521708eeb6',
        # 'https://www.dabangapp.com/room/5ea1445d636ba07f16d4646c',
        # 'https://www.dabangapp.com/room/5eaf9c79fd1eed543f5dece3',
        # 'https://www.dabangapp.com/room/5eafcf02cf93057edf5a7580',
        # 'https://www.dabangapp.com/room/5ead0a60dbf9cc25f5dbf555',
        # 'https://www.dabangapp.com/room/5ea66086393fbb26ee468081',
        # 'https://www.dabangapp.com/room/5ea686a3d5d5e31f117ea693',
        # 'https://www.dabangapp.com/room/5ea6719df30e4906b9b5d1b0',
        # 'https://www.dabangapp.com/room/5eafd58d6304be5fa8748f23',
        # 'https://www.dabangapp.com/room/5e9e7a1a3275bd3dedfbadbf',
        # 'https://www.dabangapp.com/room/5ea7d2570ff5d91930f70f4d',
        # 'https://www.dabangapp.com/room/5eafe61df191f22ffb8d94a0',
        # 'https://www.dabangapp.com/room/5e8ab2d3e5b96224197411d8',
        # 'https://www.dabangapp.com/room/5ea66d43fd4c941c8c5ae5ff',
        # 'https://www.dabangapp.com/room/5eafd360c447b72e23803ddb',
        # 'https://www.dabangapp.com/room/5ea8ff8ac45498341f6be42d',
        # 'https://www.dabangapp.com/room/5e9a9586f8d6c15542e17680',
        # 'https://www.dabangapp.com/room/5eaf990eaf46cb11c5abbc2a',
        # 'https://www.dabangapp.com/room/5ea7a5e885cf0a73feb47037',
        # 'https://www.dabangapp.com/room/5ead15239044a16cfe5cab3e',
        # 'https://www.dabangapp.com/room/5ea68e4fe8ed5447ab747158',
        # 'https://www.dabangapp.com/room/5ea109f0d044dc64ec9e83c4',
        # 'https://www.dabangapp.com/room/5ea14e14caceac45b3db6f09',
        # 'https://www.dabangapp.com/room/5ea11e5b142e92049163a55e',
        # 'https://www.dabangapp.com/room/5e9a801126b6362ef9643304',
        # 'https://www.dabangapp.com/room/5eafca2f3833ca7a00da25cc',
        # 'https://www.dabangapp.com/room/5e8d636cdc19e6397ec46d1e',
        # 'https://www.dabangapp.com/room/5ea7dc2aae35516a7f932a85',
        # 'https://www.dabangapp.com/room/5ea254ea23e2d246388705c9',
        # 'https://www.dabangapp.com/room/5e8aa4778e97eb10a32212da',
        # 'https://www.dabangapp.com/room/5ea15bec9e83bd1cd30c0dd7',
        # 'https://www.dabangapp.com/room/5ea7e3a172665c054f62d3ce',
        # 'https://www.dabangapp.com/room/5e9830b9b663983579c58766',
        # 'https://www.dabangapp.com/room/5eafcef62dfb197edf36d02b',
        # 'https://www.dabangapp.com/room/5e991207f8626e52174025fa',
        # 'https://www.dabangapp.com/room/5eaf992b1d780f11c54bb16e',
        # 'https://www.dabangapp.com/room/5ea7cea62d02d7513aee1429',
        # 'https://www.dabangapp.com/room/5ea153fc23360a602a5b3dff',
        # 'https://www.dabangapp.com/room/5e993faad404b13eebefc07c',
        # 'https://www.dabangapp.com/room/5ea11daa6ad99a6b87825030',
        # 'https://www.dabangapp.com/room/5ea903aa7b2c0871b199d61b',
        # 'https://www.dabangapp.com/room/5e9a93546f87913df7e9a3c8',
        # 'https://www.dabangapp.com/room/5ea13a4941df6448833e550f',
        # 'https://www.dabangapp.com/room/5eaf8526e7a32678ece9c7c8',
        # 'https://www.dabangapp.com/room/5e9a9d28f3c5cc720adcf372',
        # 'https://www.dabangapp.com/room/5e941f861343d9304c095c33',
        # 'https://www.dabangapp.com/room/5e967dbc5448c97f566410e9',
        # 'https://www.dabangapp.com/room/5ea7d33a4a78301930ca5fbc',
        # 'https://www.dabangapp.com/room/5e9e4be7a2089e2a1ea40848',
        # 'https://www.dabangapp.com/room/5eafceeb3b36157edf8b153d',
        # 'https://www.dabangapp.com/room/5ead45deaa313e33b6a00f7a',
        # 'https://www.dabangapp.com/room/5ea14ef101a9a858d050e301',
        # 'https://www.dabangapp.com/room/5eb0d502ce206734d058f08f',
        # 'https://www.dabangapp.com/room/5e8be7742fa6cd03e13c708b',
        # 'https://www.dabangapp.com/room/5eacd13605cd3b48d260be20',
        # 'https://www.dabangapp.com/room/5ea11d665478006b87d097a9',
        # 'https://www.dabangapp.com/room/5ea123f5b5044172720f27c4',
        # 'https://www.dabangapp.com/room/5ea107a769d22940bb6dfb00',
        # 'https://www.dabangapp.com/room/5eafccc13d305e390835eacb',
        # 'https://www.dabangapp.com/room/5eaf8c40ea9772088fc9f66f',
        # 'https://www.dabangapp.com/room/5ea8f5c05d0ce16e242d4822',
        # 'https://www.dabangapp.com/room/5e9a6d46240f921ded23c612',
        # 'https://www.dabangapp.com/room/5e990448a2d17027c7d5a1be',
        # 'https://www.dabangapp.com/room/5ea8dadffd53194a5d62d0a5',
        # 'https://www.dabangapp.com/room/5e9d9148b9fe4f38991401fa',
        # 'https://www.dabangapp.com/room/5ea15bed9b68f41cd31be68f',
        # 'https://www.dabangapp.com/room/5ead0da70753cd64e0725c4d',
        # 'https://www.dabangapp.com/room/5e9f966d5bff6f69c8e5269a',
        # 'https://www.dabangapp.com/room/5ead5183833a7b1ac3dfcb8d',
        # 'https://www.dabangapp.com/room/5ea79f5cb709817b314964f0',
        # 'https://www.dabangapp.com/room/5ea945086786882fd262591c',
        # 'https://www.dabangapp.com/room/5e8c2e7efbefce1fe5167abd',
        # 'https://www.dabangapp.com/room/5ea7b08f658edb62f80dd7a7',
        # 'https://www.dabangapp.com/room/5ea8e2f50f4a936ab7e147e6',
        # 'https://www.dabangapp.com/room/5e8ab2a116fdf52419a4663e',
        # 'https://www.dabangapp.com/room/5eafd7e782fcb80d7d64fe04',
        # 'https://www.dabangapp.com/room/5eafe616e295812ffb8d2bbe',
        # 'https://www.dabangapp.com/room/5ea12196911aae727274516c',
        # 'https://www.dabangapp.com/room/5ea12d58a0489228291ef92a',
        # 'https://www.dabangapp.com/room/5ea79398be04d80f37b491db',
        # 'https://www.dabangapp.com/room/5e959ed59d092d2d947a6e82',
        # 'https://www.dabangapp.com/room/5ea7b4ec8f487f2751bc300a',
        # 'https://www.dabangapp.com/room/5eafca890eea277a0048bf78',
        # 'https://www.dabangapp.com/room/5ea67a1edf2d2f21d37dfee0',
        # 'https://www.dabangapp.com/room/5eafe6197d60eb2ffbeea70b',
        # 'https://www.dabangapp.com/room/5e9579612464e04ad27f0f71',
        # 'https://www.dabangapp.com/room/5ea8f2f851510b2cfd314ef6',
        # 'https://www.dabangapp.com/room/5e919ebcf6898d237c673810',
        # 'https://www.dabangapp.com/room/5ea6438d3df14f40108de38f',
        # 'https://www.dabangapp.com/room/5eafe61239adc62ffb9bb1ac',
        # 'https://www.dabangapp.com/room/5e8ae5dd2a140b19ad1152a0',
        # 'https://www.dabangapp.com/room/5eafd57e84d6205fa83dfdf6',
        # 'https://www.dabangapp.com/room/5ea63b1fd829bd07c1cff5f3',
        # 'https://www.dabangapp.com/room/5e990650191cf83bfeb9b2ff',
        # 'https://www.dabangapp.com/room/5eaceef8099b7d0571360f56',
        # 'https://www.dabangapp.com/room/5ea64e09937bb91fb128f28a',
        # 'https://www.dabangapp.com/room/5e95402d89c3f624a200b096',
        # 'https://www.dabangapp.com/room/5ea7d76a07d92274416faaed',
        # 'https://www.dabangapp.com/room/5ea7b97e5074091c0ac1ccb0',
        # 'https://www.dabangapp.com/room/5eafd7eb30f7610d7dca2b21',
        # 'https://www.dabangapp.com/room/5ea7e3c3ad2e4b054f2c4323',
        # 'https://www.dabangapp.com/room/5eaf9c5e271f06543f6e4d1d',
        # 'https://www.dabangapp.com/room/5ea14e016addd145b3ec8dc3',
        # 'https://www.dabangapp.com/room/5ea7da04e8dccd47fdd8872b',
        # 'https://www.dabangapp.com/room/5ea7d0d2bc08a7732f5f44eb',
        # 'https://www.dabangapp.com/room/5eaf876a801c932936216d82',
        # 'https://www.dabangapp.com/room/5ea6858ba6f3942fc7d93400',
        # 'https://www.dabangapp.com/room/5e8ff5dc57abf65d42b86d86',
        # 'https://www.dabangapp.com/room/5e8e76abab03dd31e56dcb71',
        # 'https://www.dabangapp.com/room/5e942123724aac304cd16dc8',
        # 'https://www.dabangapp.com/room/5ea6624f028aa74f53fa95e4',
        # 'https://www.dabangapp.com/room/5ea65c1e2ac2a83cdb7db18d',
        # 'https://www.dabangapp.com/room/5ea6885d490e5f4178850216',
        # 'https://www.dabangapp.com/room/5e8edff144048f63141f001c',
        # 'https://www.dabangapp.com/room/5ead47dde54b1d591c5881ff',
        # 'https://www.dabangapp.com/room/5ea93474bcb5484c35db746e',
        # 'https://www.dabangapp.com/room/5e940cdd1ce2ec3178760a38',
        # 'https://www.dabangapp.com/room/5ead050fd7ca9f3d78950322',
        # 'https://www.dabangapp.com/room/5eafb916dca9da58adb35b7f',
        # 'https://www.dabangapp.com/room/5eafe2cb322a7f6fcdd585d2',
        # 'https://www.dabangapp.com/room/5ead42acb0fcf76ef3cab03e',
        # 'https://www.dabangapp.com/room/5e8ae5ed851dda19ad8b717d',
        # 'https://www.dabangapp.com/room/5ead0bed24324c4644027077',
        # 'https://www.dabangapp.com/room/5ead42d55f1b5c6ef3d9b23c',
        # 'https://www.dabangapp.com/room/5ead19b693a8625720caebe9',
        # 'https://www.dabangapp.com/room/5e9900c05b96152a30f1836c',
        # 'https://www.dabangapp.com/room/5e9a828f0d68674507df2f6f',
        # 'https://www.dabangapp.com/room/5ea7998e00bc4609fd0f0ddb',
        # 'https://www.dabangapp.com/room/5e9146a83fb2521b2c49ecee',
        # 'https://www.dabangapp.com/room/5e95779ac7ba0c4ad2ccf748',
        # 'https://www.dabangapp.com/room/5ea672bc6da2bc06b9096894',
        # 'https://www.dabangapp.com/room/5ea7b66cc5eea5577f924f5d',
        # 'https://www.dabangapp.com/room/5eacf9a266969e57bf13d867',
        # 'https://www.dabangapp.com/room/5e93d59f0d890e350fde4db7',
        # 'https://www.dabangapp.com/room/5ead4a97264454168ccbf4e3',
        # 'https://www.dabangapp.com/room/5e97d58eaef5dd36e7d0546c',
        # 'https://www.dabangapp.com/room/5eafe2ef872c536fcd574ce4',
        # 'https://www.dabangapp.com/room/5eaf8ae0cf6382725b62d1bd',
        # 'https://www.dabangapp.com/room/5e8aac2b54de271a14e4c32e',
        # 'https://www.dabangapp.com/room/5e9d77fa86a7380414e4fe0f',
        # 'https://www.dabangapp.com/room/5ead4fe4fe27e268d4404b58',
        # 'https://www.dabangapp.com/room/5eacea45168ec43fe268c959',
        # 'https://www.dabangapp.com/room/5ea7b5c4dd687740e95f00d0',
        # 'https://www.dabangapp.com/room/5ead42c324f1986ef308fb3e',
        # 'https://www.dabangapp.com/room/5eafc65b0c2de628e3167275',
        # 'https://www.dabangapp.com/room/5ea678fc7cc1f313a06db646',
        # 'https://www.dabangapp.com/room/5ea126699cd5531b825459c0',
        # 아파트 종료

        'https://www.dabangapp.com/room/5ea8fb2f1e40cc1e1d594582',
        'https://www.dabangapp.com/room/5e996a9b7accce730023773e',
        'https://www.dabangapp.com/room/5e9435995c3ac1609a8fd908',
        'https://www.dabangapp.com/room/5eabf168605bd801ac2ce221',
        'https://www.dabangapp.com/room/5eafc4e64cb2280d81848220',
        'https://www.dabangapp.com/room/5e6f0321aeeb591276221de3',
        'https://www.dabangapp.com/room/5df1ea294eac3d7bfabcba03',
        'https://www.dabangapp.com/room/5eb0f25266446d61d3bcb825',
        'https://www.dabangapp.com/room/5eacfec2cf86d6027db476f5',
        'https://www.dabangapp.com/room/5ead4bdc930f1253b46d3624',
        'https://www.dabangapp.com/room/5eafbac735016b1f1fdf1f41',
        'https://www.dabangapp.com/room/5e994fc856dddc1856281d59',
        'https://www.dabangapp.com/room/5ea78100275cd339f923bbf5',
        'https://www.dabangapp.com/room/5eacc989737755348a1f036b',
        'https://www.dabangapp.com/room/5d8ee7ac7fa17e2f2267239a',
        'https://www.dabangapp.com/room/5d64b386c2523c16a42f3d07',
        'https://www.dabangapp.com/room/5ea5b918f8f81035004116ce',
        'https://www.dabangapp.com/room/5e9034ed4ef6ae3420ccbfb7',
        'https://www.dabangapp.com/room/5eab6f68ebb0ab04d5b09645',
        'https://www.dabangapp.com/room/5ea65cb7aa04a31d3ce76eb4',
        'https://www.dabangapp.com/room/5e9192b1afa34c2320474d61',
        'https://www.dabangapp.com/room/5ea781059396b45c79af37e2',
        'https://www.dabangapp.com/room/5e9d038f618ea701e1304f33',
        'https://www.dabangapp.com/room/5ea0fcfd27599121780b30b1',
        'https://www.dabangapp.com/room/5e8ace5e7702c43897f858ac',
        'https://www.dabangapp.com/room/5eaf9b9b88cf4849d008040d',
        'https://www.dabangapp.com/room/5eb0f98c664e4766d7027408',
        'https://www.dabangapp.com/room/5ea816f32998671e96b1e1ea',
        'https://www.dabangapp.com/room/5eafc339eced9c2814ab0916',
        'https://www.dabangapp.com/room/5e8f01b3cec5d415e90d4cf6',
        'https://www.dabangapp.com/room/5eb11b099743495e5854375b',
        'https://www.dabangapp.com/room/5e4b99581a00fb457ff0ef63',
        'https://www.dabangapp.com/room/5e58feb4bab02104722d161f',
        'https://www.dabangapp.com/room/5ead203c9687452e78d8ed34',
        'https://www.dabangapp.com/room/5ead4a09323dd0565f86b4e3',
        'https://www.dabangapp.com/room/5e9eb0fc7145c11ebb232db9',
        'https://www.dabangapp.com/room/5ea0f58193c1372ac2df539f',
        'https://www.dabangapp.com/room/5e0f3718d96bea310291e09a',
        'https://www.dabangapp.com/room/5e3845a2d7447c3fabc904e3',
        'https://www.dabangapp.com/room/5eafd7b2f3f6303bdf4591f3',
        'https://www.dabangapp.com/room/5e9fd19bdea9fc5a7d8f5173',
        'https://www.dabangapp.com/room/5e99601abc1a2e63758d1968',
        'https://www.dabangapp.com/room/5ea931e53e078172cff52cac',
        'https://www.dabangapp.com/room/5ea65cbc38e46c2fdc92a4ef',
        'https://www.dabangapp.com/room/5e99104de7921f1d798272a3',
        'https://www.dabangapp.com/room/5ea7ba9ef5156f6618c42a7a',
        'https://www.dabangapp.com/room/5df1eb02d5887d7930797275',
        'https://www.dabangapp.com/room/5e9d03b0eb4f8f27a0b1c0a2',
        'https://www.dabangapp.com/room/5ea64a5363265c685a5f9db0',
        'https://www.dabangapp.com/room/5eafb36b47dbb21ec566f4f4',
        'https://www.dabangapp.com/room/5ea3ce6350f429521fa8f957',
        'https://www.dabangapp.com/room/5e97be37ebb9bb57a7d35d5f',
        'https://www.dabangapp.com/room/5ea94cc2efc68d20d4229297',
        'https://www.dabangapp.com/room/5e9fbc3505ff823c392d4d3a',
        'https://www.dabangapp.com/room/5ea934f7cb0ad47994b296df',
        'https://www.dabangapp.com/room/5e992d3359f24d63d2c5afc2',
        'https://www.dabangapp.com/room/5ea780fb19336f5c7942daf1',
        'https://www.dabangapp.com/room/5e93ec571087be6c9d348d9c',
        'https://www.dabangapp.com/room/5eafbefa64c5a51add57d9ec',
        'https://www.dabangapp.com/room/5ea8f095a5107a09ca444b3f',
        'https://www.dabangapp.com/room/5e33bb027bfab713de85a774',
        'https://www.dabangapp.com/room/5ddf97f4224cdd3567cebf9b',
        'https://www.dabangapp.com/room/5db78bcdeaa0e9359de71c0f',
        'https://www.dabangapp.com/room/5eaa3b2f82bc382d2031d35a',
        'https://www.dabangapp.com/room/5e9c6094fbacbb09194f76ba',
        'https://www.dabangapp.com/room/5e9d038861e7bf04feff40cc',
        'https://www.dabangapp.com/room/5e3bdb7635fc9778dae9d35a',
        'https://www.dabangapp.com/room/5e19204fd1e8ba59c8b5d7f4',
        'https://www.dabangapp.com/room/5ddcfaec6e8a987c8a9e65e1',
        'https://www.dabangapp.com/room/5e6132798c88164b71a43b63',
        'https://www.dabangapp.com/room/5e61de5954444f17b12b891d',
        'https://www.dabangapp.com/room/5ea909faf296e4162a46f190',
        'https://www.dabangapp.com/room/5de1e3dcbff13320f9e8c246',
        'https://www.dabangapp.com/room/581ae8a8f7f1fe26fd7d65f0',
        'https://www.dabangapp.com/room/5e9a9ccf17b6ea61206f3133',
        'https://www.dabangapp.com/room/5e996005faf976637565726a',
        'https://www.dabangapp.com/room/5ea69c3da587b143dda04c7a',
        'https://www.dabangapp.com/room/5e3cfc049d81167ed198e975',
        'https://www.dabangapp.com/room/5eaa93899305d6648a05c13e',
        'https://www.dabangapp.com/room/5e268a6db427ae304ec68e3f',
        'https://www.dabangapp.com/room/5e3ba7b9610c7e1f02caba75',
        'https://www.dabangapp.com/room/5ea3d81ed930955fb1abd57f',
        'https://www.dabangapp.com/room/5e8c077fc6addb21400412cb',
        'https://www.dabangapp.com/room/5e9c62555563ac2c0f02f549',
        'https://www.dabangapp.com/room/5e7c52a336e37e1fa669f93e',
        'https://www.dabangapp.com/room/5ead53ffd8816651802ed2c1',
        'https://www.dabangapp.com/room/5c5d8557e98ed333425a3cb4',
        'https://www.dabangapp.com/room/5e9a69580a6e2a1917b16a4f',
        'https://www.dabangapp.com/room/5e659c74f2a3ac415c367599',
        'https://www.dabangapp.com/room/5ea7a2302db1071c18cc2c5a',
        'https://www.dabangapp.com/room/5e92d088e2f8f970339a1816',
        'https://www.dabangapp.com/room/5ea11deceb27865ced4c9866',
        'https://www.dabangapp.com/room/5d89b7deb3be6628c11e79d4',
        'https://www.dabangapp.com/room/5eaaaaf7fcb72257be132297',
        'https://www.dabangapp.com/room/5c8319179435f455bfadb906',
        'https://www.dabangapp.com/room/5e93d057bc9e1620963edf68',
        'https://www.dabangapp.com/room/5e24669efd66bf3f32346a69',
        'https://www.dabangapp.com/room/5dc282ff3c2c224b0a79097c',
        'https://www.dabangapp.com/room/5e8d36c5643ef26fe5d7a23a',
        'https://www.dabangapp.com/room/5e9960100d9b5158f03c1317',
        'https://www.dabangapp.com/room/5eacc984a94891348a00f90a',
        'https://www.dabangapp.com/room/5e577c56e868473adfb353ff',
        'https://www.dabangapp.com/room/5d07c75b3742fe7603630b43',
        'https://www.dabangapp.com/room/5ea9f4d5b8eca22ccb959f77',
        'https://www.dabangapp.com/room/5e8e89360988e55bd5c27df0'
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
            print('total_citizen', total_citizen)

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
            print('min_max_floor', min_max_floor)

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

        driver.get(dabang_url)
        time.sleep(1)
        # 아파트 단지 정보 종료.

        post = PostRoom.objects.get_or_create(
            broker=broker_ins[0],
            complex=complex_obj,
            type=post_type,
            description=description,
            address=address_ins,
            salesForm=salesform_ins,
            lat=lat,
            lng=lng,
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
