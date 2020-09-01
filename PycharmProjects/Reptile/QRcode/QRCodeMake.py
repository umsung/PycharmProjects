import qrcode

# Link for website
input_data = "http://card.wine-world.com/酒款ID"

# 酒瓶后面的二维码现在只支持三种格式：
# http://card.wine-world.com/GUID/年份
# http://card.wine-world.com/酒款ID
# http://minimall.wine-world.com/xproduct/酒款ID


# Creating an instance of qrcode
qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)

qr.add_data(input_data)
qr.make(fit=True)

img = qr.make_image(fill='black', back_color='white')
img.save('qrcode001.png')