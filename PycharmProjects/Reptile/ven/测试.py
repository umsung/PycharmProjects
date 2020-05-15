import re
from fontTools.ttLib import TTFont


html='''
<div class="col more">电话：
   <d class="vhkbvu"></d> 
   <d class="vhk08k"></d> 
   <d class="vhk08k"></d> 
   <d class="">-</d>
   "1-" 
   <d class="vhk84t"></d> 
   <d class="vhk6zl"></d> 
   "1"
   <d class="vhkqsc"></d> 
   <d class="vhkqsc"></d> 
   <d class="vhk6zl"></d> 
</div>'''

code = 'vhk6zl'
a=re.findall('<d class="(.*?)">|(\d+)', html, re.S)

css = '''d[class^="vhk"] {
  width: 14px;
  height: 30px;
  margin-top: -9px;
  background-image: url(../font/food.svg);
  background-repeat: no-repeat;
  display: inline-block;
  vertical-align: middle;
  margin-left: -6px;
}
.vhk08k {
  background: -274px -141px;
}
.vhk6zl {
  background: -7px -15px;
}
.vhk0ao {
  background: -133px -97px;
}
.vhk9or {
  background: -330px -141px;
}
.vhkfln {
  background: -428px -15px;
}
.vhkbvu {
  background: -386px -97px;
}
.vhk84t {
  background: -176px -141px;
}
.vhkvxd {
  background: -246px -141px;
}
.vhkqsc {
  background: -288px -141px;
}
.vhkjj4 {
  background: -316px -141px;
}
.vhk0f1 {
  background: -316px -97px;
}'''

b=re.findall(code+'.*?background: -(.*?)px -(.*?)px;',css,re.S)
print(a,b)

fontObj = TTFont('D:/用户目录/下载/b536766c.woff')
# fontObj.saveXML('D:/用户目录/下载/b536766c.html')
unilist = fontObj.getGlyphOrder()
