import pyqrcode
qr = pyqrcode.create("HORN O.K. PLEASE.")
qr.png("horn.png", scale=6)
from qrtools.qrtools import QR
qr = QR()
qr.decode("horn.png")
print(qr.data)