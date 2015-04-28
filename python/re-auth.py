"""
Stupid simple program to take a google authenticator database
and dump it back out as QR-Codes
"""
import otpauth
import sqlite3
import qrcode
from collections import namedtuple

row = namedtuple('auth', 'id email secret counter type provider issuer original_name')

sqlite3.connect('./databases')
cursor = conn.execute('select * from accounts')
auths = [row(x) for x in cursor.fetchall()]

def to_qr(auth):
    otp = otpauth.OtpAuth(auth.secret)
    uri = otp.to_uri('totp', auth.email, auth.original_name)
    img = qrcode.make(uri)
    return img

for i, auth in enumerate(auths):
    to_qr(auth).save('/tmp/%d.png' % i)
