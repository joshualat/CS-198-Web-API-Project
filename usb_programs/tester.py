from secure_web_connection import *
import datetime

swc = SecureWebConnection("http://localhost:8000/","\x90\xe6\x8b\x80b\xf2\xbecq\x88\xdd\xc2j\xde1\xb0\x19B\x01v\xa7glY\x96\xf6\x10\xa1&Ir\xf8")
print swc.start()

m1 = {
    'action':'username_exists',
    'data':{
        'username':'josh'
    }
}

m2 = {
    'action':'register',
    'data':{
        'username':'josh',
        'first_name':'Joshua',
        'last_name':'Lat',
        'email':'akosijoshualat@yahoo.com',
        'sex':'M',
        'birthdate':datetime.datetime(1990,4,17),
    }
}

m3 = {
    'action':'edit_user_info',
    'data':{
        'username':'josh',
        'first_name':'Joshua',
        'last_name':'Lat',
        'email':'akosijoshualat@gmail.com',
        'sex':'M',
        'birthdate':datetime.datetime(1990,4,17),
    }
}

m4 = {
    'action':'get_user_info',
    'data':{}
}

m5 = {
    'action':'login',
    'data':{}
}

m6 = {
    'action':'logout',
    'data':{}
}

print swc.secure_connection(m3)
print swc.secure_connection(m5)
#print swc.secure_connection(m6)
swc.end()
