from secure_web_connection import *
swc = SecureWebConnection("http://localhost:8000/","\x90\xe6\x8b\x80b\xf2\xbecq\x88\xdd\xc2j\xde1\xb0\x19B\x01v\xa7glY\x96\xf6\x10\xa1&Ir\xf8")
swc.start()
print swc.secure_connection("Joshua")
swc.end()
