# -*- coding: utf-8 -*-
import requests
import scrapy
from lxml import etree
import re
from fontTools.ttLib import TTFont

class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'
    allowed_domains = ['kuaishou.com']
    start_urls = ['https://live.kuaishou.com/search/author?keyword=%E6%AF%8D%E5%A9%B4']

    def parse(self, response):
        # print(response.text)
        # node_list = response.xpath('//*[@class="author-card"]')
        # for node in node_list:
        #     # data = node.xpath('//p[@class="profile-card-user-info-counts"]/text()').extract()
        #     # # print(data)
        #     # adata = ''.join(node.extract())
        #     # item = {}
        #     #
        #     #
        #     #
        #     # bdata = re.search('<p class="profile-card-user-info-counts" data-v-74e18046>(.*?)</p>', adata, re.S)
        #     # item['bdata'] = bdata.group(1).strip().encode('unicode_escape')
        #     # a = item['bdata'][:-28].replace(b'\\u', b'\\')
        #     # a = a[:-28].replace(b'\\', b';').decode('utf-8').upper()
        #     # print(item['bdata'])
        #     # print(a)
        #     # # yield item


        next_url = response.xpath('//div[@class="search-action"]/a[2]/@href').extract_first()
        yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse)


        font_url = re.findall(r"url\('(https:.*\.ttf)'\)", response.text)[0]
        with open('on_kuaishou.ttf', 'wb') as f:
            f.write(requests.get(font_url).content)


        base_font = TTFont('base_kuaishou.ttf')
        base_font.saveXML('base_kuaishou.xml')
        base_uni = base_font.getGlyphOrder()

        dict_font = {'uniAACB': '4', 'uniABCD': '3', 'uniACDD': '0', 'uniAEFB': '8', 'uniAFBC': '6',
                     'uniBBCA': '1', 'uniBDCA': '5', 'uniBFEE': '9', 'uniCCAC': '2', 'uniCFBA': '7'}


        online_font = TTFont('on_kuaishou.ttf')
        on_dict= online_font.getBestCmap()


        selector = etree.HTML(response.body.decode('utf-8'))
        node_list = selector.xpath('//*[@class="author-card"]')
        for node in node_list:
            item = {}
            item['title'] = node.xpath('.//div[@class="profile-card-user-info-intro"]/@title')[0]

            i = etree.tostring(node).decode('utf-8')
            # print(i)
          #  data = re.search('<p class="profile-card-user-info-counts" data-v-74e18046="">(.*?)</p>', i, re.S)
            data = re.search('<p class="profile-card-user-info-counts" data-v-74e18046="">\s+(.*?)\s+(.*?)\s+(.*?)\s+</p>', i, re.S)

            # print(data.group())
            # print(data.group(1)[:-28])
            # print(data.group(2)[:-28])

            fans = data.group(1)[:-28].strip()
            fans = re.sub('&#', '', fans)
            follower = data.group(2)[:-28].strip()
            follower = re.sub('&#', '', follower)
            prod = data.group(3)[:-16].strip()
            prod = re.sub('&#', '', prod)
            print(fans)
            print(follower)
            print(prod)
            item['fans'] = jiemiStr(online_font,base_font,fans)
            item['prod'] = jiemiStr(online_font,base_font,prod)
            item['follower'] = jiemiStr(online_font,base_font,follower)
            yield item


def newMapDict(online_font,base_font,code):
     '''
        根据每个加密编码，单个解密
    '''
    dict_font = {'uniAACB': '4', 'uniABCD': '3', 'uniACDD': '0', 'uniAEFB': '8', 'uniAFBC': '6',
                    'uniBBCA': '1', 'uniBDCA': '5', 'uniBFEE': '9', 'uniCCAC': '2', 'uniCFBA': '7'}
    temp={}
    list_base_uni = base_font.getGlyphOrder()[1:]
    one_online_uni = online_font.getBestCmap()[int(code)]
    one_online_obj = online_font['glyf'][one_online_uni]
    for one_base_uni in list_base_uni:
        if base_font['glyf'][one_online_uni] == one_online_obj:
            return dict_font[one_base_uni]


def jiemiStr(online_font,base_font,jiami_str):
    item=[]
    if  jiami_str != '':
        if '.' in jiami_str:
            jiami_str = re.sub('\.', '.;', jiami_str)
            jiami_str = jiami_str.split(';')
            for f in jiami_str:
                if f != '':
                    if f == '.' or f == 'w':
                        item.append(f)
                    else:
                        item.append(newMapDict(online_font,base_font,f))
        else:
            jiami_str = jiami_str.split(';')
            for f in jiami_str:
                if f != '':
                    if f == '.' or f == 'w':
                        item.append(f)
                    else:
                        item.append(newMapDict(online_font,base_font,f))
    item = ''.join(item)
    return item


def jiemi(online_font, base_font, f, dict_font):
    # 通过2进制code码拿到对应键名
    on_uni = online_font.getBestCmap()[int(f)]
    # 通过键名拿到字体形状
    on_obj = online_font['glyf'][on_uni]
    for bs_uni in base_font.getGlyphOrder():
        if base_font['glyf'][bs_uni] == on_obj:
            return dict_font[bs_uni]


def jiemiStr2(online_font,base_font,jiami_text):
    '''
        先构造出网页加密的编码和正确字符的映射关系，再整体替换
    '''

    temp ={}
    dict_font = {'uniAACB': '4', 'uniABCD': '3', 'uniACDD': '0', 'uniAEFB': '8', 'uniAFBC': '6',
                    'uniBBCA': '1', 'uniBDCA': '5', 'uniBFEE': '9', 'uniCCAC': '2', 'uniCFBA': '7'}
    online_uni_list = online_font.getGlyphOrder()[1:]
    base_uni_list = base_font.getGlyphOrder()[1:]
    for online_uni in online_uni_list:
        online_obj = online_font['glyf'][online_uni]
        for base_uni in base_uni_list:
            base_obj = base_font['glyf'][base_uni]
            if online_obj == base_obj:
                temp['&#x'+online_uni[3:].lower()+';'] = dict_font[base_uni]
    for k,v in temp.items():
        jiami_text = re.sub(k,v,jiami_text)
    return jiami_text

# # 解析字体库
# temp = {}
# for i in range(10):
#     onlineGlyph = onlineFonts['glyf'][uni_list[i]]
#     for j in range(10):
#         baseGlyph = baseFonts['glyf'][base_fonts[j]]
#         if onlineGlyph == baseGlyph:
#             temp["&#x" + uni_list[i][3:].lower() + ';'] = base_nums[j]
#
# # 字符替换  把temp.kes 拼成(&#xABCD;|&#XSDFG|....)
# pat = '(' + '|'.join(temp.keys()) + ')'
#
# # 在根据pat 把对应的key.values替换
# response_index = re.sub(pat, lambda x: temp[x.group()],     response_index)
