import pyqrcode
qr = pyqrcode.create("test1")
qr.png("test1.png", scale=6)

