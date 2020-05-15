import re,requests
from lxml import etree

url_css = 'http://www.porters.vip/confusion/css/food.css' 
url_svg = 'http://www.porters.vip/confusion/font/food.svg'

class SVG():
    def __init__(self):
        self.url_css = 'http://www.porters.vip/confusion/css/food.css' 
        self.url_svg = 'http://www.porters.vip/confusion/font/food.svg'
        self.posList = [('vhkbvu', ''), ('vhk08k', ''), ('vhk08k', ''), ('', ''), ('', '1'), ('vhk84t', ''), ('vhk6zl', ''), ('', '1'), ('vhkqsc', ''), ('vhkqsc', ''), ('vhk6zl', '')]

    def get_code(self):
        code_list = []
        for tu in self.posList:
            code_list.append(tu[0] if tu[0] !='' else tu[1])
        return code_list

    def get_html(self,url):
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.content
        return html

    def get_pos(self,code,css_html):
        pos = re.findall(code+'.*?background: -(.*?)px -(.*?)px;',css_html.decode('utf-8'),re.S)
        return pos[0]

    def get_num(self,svg,pos_x,pos_y):
        selector = etree.HTML(svg)
        y_list = selector.xpath('//text/@y')
        y_list = [int(y) for y in y_list if int(y) > pos_y]
        y = min(y_list)
        x = selector.xpath('//text[@y={}]/@x'.format(y))[0]
        text = selector.xpath('//text[@y={}]/text()'.format(y))[0]
        dict_x = dict(zip(x.split(),list(text)))
        print(type(text),dict_x)
        return dict_x[pos_x]

    def main(self):
        svg_html = self.get_html(self.url_svg)
        css_html = self.get_html(self.url_css)
        item = []
        for code in self.get_code():
            if len(code) == 1:
                item.append(code)
            else:
                pos_x,pos_y=self.get_pos(code,css_html)
                pos_x =int(pos_x)+6 if int(pos_x) % 2 == 0 else int(pos_x)+7
                num = self.get_num(svg_html,str(pos_x),int(pos_y))
                item.append(num)
        return ''.join(item)

if __name__ == "__main__":
    svg = SVG()
    print(svg.main())
